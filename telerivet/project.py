
from .entity import Entity
        
class Project(Entity):
    """
    Represents a Telerivet project.
    
    Provides methods for sending and scheduling messages, as well as accessing,
    creating and updating a variety of entities, including contacts, messages, scheduled messages,
    groups, labels, phones, services, and data tables.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the project
          * Read-only
      
      - name
          * Name of the project
          * Updatable via API
      
      - timezone_id
          * Default TZ database timezone ID; see
              <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this project
          * Updatable via API
      
    """

    def getOrCreateGroup(self, name):
        """
        Gets or creates a group by name.
        
        Arguments:
          - name
              * Name of the group
              * Required
          
        Returns:
            Group
        """
        from .group import Group
        return Group(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/groups", {'name': name}))    
        
    def getOrCreateLabel(self, name):
        """
        Gets or creates a label by name.
        
        Arguments:
          - name (Name of the label)
          
        Returns:
            Label
        """
        from .label import Label
        return Label(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/labels", {'name': name}))
    
    _has_custom_vars = True

    def sendMessage(self, **options):
        """
        Sends one message (SMS or USSD request).
        
        Arguments:
              * Required
            
            - content
                * Content of the message to send
                * Required if sending SMS message
            
            - to_number (string)
                * Phone number to send the message to
                * Required if contact_id not set
            
            - contact_id
                * ID of the contact to send the message to
                * Required if to_number not set
            
            - route_id
                * ID of the phone or route to send the message from
                * Default: default sender phone ID for your project
            
            - status_url
                * Webhook callback URL to be notified when message status changes
            
            - status_secret
                * POST parameter 'secret' passed to status_url
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content
                * Default: false
            
            - label_ids (array)
                * List of IDs of labels to add to this message
            
            - message_type
                * Type of message to send
                * Allowed values: sms, ussd
                * Default: sms
            
            - priority (int)
                * Priority of the message (currently only observed for Android phones). Telerivet
                    will attempt to send messages with higher priority numbers first (for example, so
                    you can prioritize an auto-reply ahead of a bulk message to a large group).
                * Default: 1
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/messages/send", options))

    def sendMessages(self, **options):
        """
        Sends an SMS message (optionally with mail-merge templates) to a group or a list of up to
        500 phone numbers
        
        Arguments:
              * Required
            
            - content
                * Content of the message to send
                * Required
            
            - group_id
                * ID of the group to send the message to
                * Required if to_numbers not set
            
            - to_numbers (array of strings)
                * List of up to 500 phone numbers to send the message to
                * Required if group_id not set
            
            - route_id
                * ID of the phone or route to send the message from
                * Default: default sender phone ID
            
            - status_url
                * Webhook callback URL to be notified when message status changes
            
            - label_ids (array)
                * Array of IDs of labels to add to all messages sent (maximum 5)
            
            - status_secret
                * POST parameter 'secret' passed to status_url
            
            - exclude_contact_id
                * Optionally excludes one contact from receiving the message (only when group_id is
                    set)
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content
                * Default: false
          
        Returns:
            (associative array)
              - count_queued (int)
                  * Number of messages queued to send
              
        """
        return self._api.doRequest("POST", self.getBaseApiPath() + "/messages/send_batch", options)

    def scheduleMessage(self, **options):
        """
        Schedules an SMS message to a group or single contact
        
        Arguments:
              * Required
            
            - content
                * Content of the message to schedule
                * Required
            
            - group_id
                * ID of the group to send the message to
                * Required if to_number not set
            
            - to_number (string)
                * Phone number to send the message to
                * Required if group_id not set
            
            - start_time (UNIX timestamp)
                * The time that the message will be sent (or first sent for recurring messages)
                * Required if start_time_offset not set
            
            - start_time_offset (int)
                * Number of seconds from now until the message is sent
                * Required if start_time not set
            
            - rrule
                * A recurrence rule describing the how the schedule repeats, e.g. 'FREQ=MONTHLY' or
                    'FREQ=WEEKLY;INTERVAL=2'; see <https://tools.ietf.org/html/rfc2445#section-4.3.10>.
                    (UNTIL is ignored; use end_time parameter)
                * Default: COUNT=1 (one-time scheduled message, does not repeat)
            
            - route_id
                * ID of the phone or route to send the message from
                * Default: default sender phone ID
            
            - message_type
                * Type of message to send
                * Allowed values: sms, ussd
                * Default: sms
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content
                * Default: false
            
            - label_ids (array)
                * Array of IDs of labels to add to the sent messages (maximum 5)
            
            - timezone_id
                * TZ database timezone ID; see
                    <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>
                * Default: project default timezone
            
            - end_time (UNIX timestamp)
                * Time after which a recurring message will stop (not applicable to non-recurring
                    scheduled messages)
            
            - end_time_offset (int)
                * Number of seconds from now until the recurring message will stop
          
        Returns:
            ScheduledMessage
        """
        from .scheduledmessage import ScheduledMessage
        return ScheduledMessage(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/scheduled", options))

    def getOrCreateContact(self, **options):
        """
        Gets OR creates and possibly updates a contact by name or phone number.
        
        If a phone number is provided, Telerivet will search for an existing
        contact with that phone number (including suffix matches to allow finding contacts with
        phone numbers in a different format).
        
        If a phone number is not provided but a name is provided, Telerivet
        will search for a contact with that exact name (case insensitive).
        
        If no existing contact is found, a new contact will be created.
        
        Then that contact will be updated with any parameters provided
        (name, phone_number, and vars).
        
        Arguments:
              * Required
            
            - name
                * Name of the contact
                * Required if phone_number not set
            
            - phone_number
                * Phone number of the contact
                * Required if name not set
            
            - vars (dict)
                * Custom variables and values to update on the contact
          
        Returns:
            Contact
        """
        from .contact import Contact
        return Contact(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/contacts", options))

    def queryContacts(self, **options):
        """
        Queries contacts within this project.
        
        Arguments:
            
            - name
                * Filter contacts by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - phone_number
                * Filter contacts by phone number
                * Allowed modifiers: phone_number[ne], phone_number[prefix],
                    phone_number[not_prefix], phone_number[gte], phone_number[gt], phone_number[lt],
                    phone_number[lte]
            
            - time_created (UNIX timestamp)
                * Filter contacts by time created
                * Allowed modifiers: time_created[ne], time_created[min], time_created[max]
            
            - last_message_time (UNIX timestamp)
                * Filter contacts by last time a message was sent or received
                * Allowed modifiers: last_message_time[exists], last_message_time[ne],
                    last_message_time[min], last_message_time[max]
            
            - vars (dict)
                * Filter contacts by value of a custom variable (e.g. vars[email], vars[foo], etc.)
                * Allowed modifiers: vars[foo][exists], vars[foo][ne], vars[foo][prefix],
                    vars[foo][not_prefix], vars[foo][gte], vars[foo][gt], vars[foo][lt], vars[foo][lte],
                    vars[foo][min], vars[foo][max]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name, phone_number, last_message_time
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Contact)
        """
        from .contact import Contact
        return self._api.newApiCursor(Contact, self.getBaseApiPath() + "/contacts", options)

    def getContactById(self, id):
        """
        Gets a contact by ID.
        
        Note: This does not make any API requests until you access a property of the Contact.
        
        Arguments:
          - id
              * ID of the contact
              * Required
          
        Returns:
            Contact
        """
        from .contact import Contact
        return Contact(self._api, {'project_id': self.id, 'id': id}, False)

    def queryPhones(self, **options):
        """
        Queries phones within this project.
        
        Arguments:
            
            - name
                * Filter phones by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - phone_number
                * Filter phones by phone number
                * Allowed modifiers: phone_number[ne], phone_number[prefix],
                    phone_number[not_prefix], phone_number[gte], phone_number[gt], phone_number[lt],
                    phone_number[lte]
            
            - last_active_time (UNIX timestamp)
                * Filter phones by last active time
                * Allowed modifiers: last_active_time[exists], last_active_time[ne],
                    last_active_time[min], last_active_time[max]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name, phone_number
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Phone)
        """
        from .phone import Phone
        return self._api.newApiCursor(Phone, self.getBaseApiPath() + "/phones", options)

    def getPhoneById(self, id):
        """
        Gets a phone by ID.
        
        Note: This does not make any API requests until you access a property of the Phone.
        
        Arguments:
          - id
              * ID of the phone - see <https://telerivet.com/dashboard/api>
              * Required
          
        Returns:
            Phone
        """
        from .phone import Phone
        return Phone(self._api, {'project_id': self.id, 'id': id}, False)

    def queryMessages(self, **options):
        """
        Queries messages within this project.
        
        Arguments:
            
            - direction
                * Filter messages by direction
                * Allowed values: incoming, outgoing
            
            - message_type
                * Filter messages by message_type
                * Allowed values: sms, mms, ussd, call
            
            - source
                * Filter messages by source
                * Allowed values: phone, provider, web, api, service, webhook, scheduled
            
            - starred (bool)
                * Filter messages by starred/unstarred
            
            - status
                * Filter messages by status
                * Allowed values: ignored, processing, received, sent, queued, failed,
                    failed_queued, cancelled, delivered, not_delivered
            
            - time_created[min] (UNIX timestamp)
                * Filter messages created on or after a particular time
            
            - time_created[max] (UNIX timestamp)
                * Filter messages created before a particular time
            
            - contact_id
                * ID of the contact who sent/received the message
            
            - phone_id
                * ID of the phone that sent/received the message
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Message)
        """
        from .message import Message
        return self._api.newApiCursor(Message, self.getBaseApiPath() + "/messages", options)

    def getMessageById(self, id):
        """
        Gets a message by ID.
        
        Note: This does not make any API requests until you access a property of the Message.
        
        Arguments:
          - id
              * ID of the message
              * Required
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, {'project_id': self.id, 'id': id}, False)

    def queryGroups(self, **options):
        """
        Queries groups within this project.
        
        Arguments:
            
            - name
                * Filter groups by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Group)
        """
        from .group import Group
        return self._api.newApiCursor(Group, self.getBaseApiPath() + "/groups", options)

    def getGroupById(self, id):
        """
        Gets a group by ID.
        
        Note: This does not make any API requests until you access a property of the Group.
        
        Arguments:
          - id
              * ID of the group
              * Required
          
        Returns:
            Group
        """
        from .group import Group
        return Group(self._api, {'project_id': self.id, 'id': id}, False)

    def queryLabels(self, **options):
        """
        Queries labels within this project.
        
        Arguments:
            
            - name
                * Filter labels by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Label)
        """
        from .label import Label
        return self._api.newApiCursor(Label, self.getBaseApiPath() + "/labels", options)

    def getLabelById(self, id):
        """
        Gets a label by ID.
        
        Note: This does not make any API requests until you access a property of the Label.
        
        Arguments:
          - id (ID of the label)
              * Required
          
        Returns:
            Label
        """
        from .label import Label
        return Label(self._api, {'project_id': self.id, 'id': id}, False)

    def queryDataTables(self, **options):
        """
        Queries data tables within this project.
        
        Arguments:
            
            - name
                * Filter data tables by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of DataTable)
        """
        from .datatable import DataTable
        return self._api.newApiCursor(DataTable, self.getBaseApiPath() + "/tables", options)

    def getDataTableById(self, id):
        """
        Gets a data table by ID.
        
        Note: This does not make any API requests until you access a property of the DataTable.
        
        Arguments:
          - id (ID of the data table)
              * Required
          
        Returns:
            DataTable
        """
        from .datatable import DataTable
        return DataTable(self._api, {'project_id': self.id, 'id': id}, False)

    def queryScheduledMessages(self, **options):
        """
        Queries scheduled messages within this project.
        
        Arguments:
            
            - message_type
                * Filter scheduled messages by message_type
                * Allowed values: sms, mms, ussd, call
            
            - time_created (UNIX timestamp)
                * Filter scheduled messages by time_created
                * Allowed modifiers: time_created[ne], time_created[min], time_created[max]
            
            - next_time (UNIX timestamp)
                * Filter scheduled messages by next_time
                * Allowed modifiers: next_time[exists], next_time[ne], next_time[min],
                    next_time[max]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of ScheduledMessage)
        """
        from .scheduledmessage import ScheduledMessage
        return self._api.newApiCursor(ScheduledMessage, self.getBaseApiPath() + "/scheduled", options)

    def getScheduledMessageById(self, id):
        """
        Gets a scheduled message by ID.
        
        Note: This does not make any API requests until you access a property of the
        ScheduledMessage.
        
        Arguments:
          - id (ID of the scheduled message)
              * Required
          
        Returns:
            ScheduledMessage
        """
        from .scheduledmessage import ScheduledMessage
        return ScheduledMessage(self._api, {'project_id': self.id, 'id': id}, False)

    def queryServices(self, **options):
        """
        Queries services within this project.
        
        Arguments:
            
            - name
                * Filter services by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - active (bool)
                * Filter services by active/inactive state
            
            - context
                * Filter services that can be invoked in a particular context
                * Allowed values: message, contact, project, receipt
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, priority, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Service)
        """
        from .service import Service
        return self._api.newApiCursor(Service, self.getBaseApiPath() + "/services", options)

    def getServiceById(self, id):
        """
        Gets a service by ID.
        
        Note: This does not make any API requests until you access a property of the Service.
        
        Arguments:
          - id (ID of the service)
              * Required
          
        Returns:
            Service
        """
        from .service import Service
        return Service(self._api, {'project_id': self.id, 'id': id}, False)

    def queryReceipts(self, **options):
        """
        Queries mobile money receipts within this project.
        
        Arguments:
            
            - tx_id
                * Filter receipts by transaction ID
            
            - tx_type
                * Filter receipts by transaction type
                * Allowed values: receive_money, send_money, pay_bill, deposit, withdrawal,
                    airtime_purchase, balance_inquiry, reversal
            
            - tx_time (UNIX timestamp)
                * Filter receipts by transaction time
                * Allowed modifiers: tx_time[ne], tx_time[min], tx_time[max]
            
            - name
                * Filter receipts by other person's name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - phone_number
                * Filter receipts by other person's phone number
                * Allowed modifiers: phone_number[ne], phone_number[prefix],
                    phone_number[not_prefix], phone_number[gte], phone_number[gt], phone_number[lt],
                    phone_number[lte]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of MobileMoneyReceipt)
        """
        from .mobilemoneyreceipt import MobileMoneyReceipt
        return self._api.newApiCursor(MobileMoneyReceipt, self.getBaseApiPath() + "/receipts", options)

    def getReceiptById(self, id):
        """
        Gets a mobile money receipt by ID.
        
        Note: This does not make any API requests until you access a property of the
        MobileMoneyReceipt.
        
        Arguments:
          - id
              * ID of the mobile money receipt
              * Required
          
        Returns:
            MobileMoneyReceipt
        """
        from .mobilemoneyreceipt import MobileMoneyReceipt
        return MobileMoneyReceipt(self._api, {'project_id': self.id, 'id': id}, False)

    def save(self):
        """
        Saves any fields or custom variables that have changed for this project.
        
        """
        super(Project, self).save()

    def getBaseApiPath(self):
        return "/projects/%(id)s" % {'id': self.id} 
