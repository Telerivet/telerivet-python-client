from .entity import Entity

class Contact(Entity):
    """
    Fields:
    
      - id (string, max 34 characters)
          * ID of the contact
          * Read-only
      
      - name
          * Name of the contact
          * Updatable via API
      
      - phone_number (string)
          * Phone number of the contact
          * Updatable via API
      
      - time_created (UNIX timestamp)
          * Time the contact was added in Telerivet
          * Read-only
      
      - time_updated (UNIX timestamp)
          * Time the contact was last updated in Telerivet
          * Read-only
      
      - send_blocked (bool)
          * True if Telerivet is blocked from sending messages to this contact
          * Updatable via API
      
      - conversation_status
          * Current status of the conversation with this contact
          * Allowed values: closed, active, handled
          * Updatable via API
      
      - last_message_time (UNIX timestamp)
          * Last time the contact sent or received a message (null if no messages have been sent
              or received)
          * Read-only
      
      - last_incoming_message_time (UNIX timestamp)
          * Last time a message was received from this contact
          * Read-only
      
      - last_outgoing_message_time (UNIX timestamp)
          * Last time a message was sent to this contact
          * Read-only
      
      - message_count (int)
          * Total number of non-deleted messages sent to or received from this contact
          * Read-only
      
      - incoming_message_count (int)
          * Number of messages received from this contact
          * Read-only
      
      - outgoing_message_count (int)
          * Number of messages sent to this contact
          * Read-only
      
      - last_message_id
          * ID of the last message sent to or received from this contact (null if no messages
              have been sent or received)
          * Read-only
      
      - default_route_id
          * ID of the phone or route that Telerivet will use by default to send messages to this
              contact (null if using project default route)
          * Updatable via API
      
      - group_ids (array of strings)
          * List of IDs of groups that this contact belongs to
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this contact
          * Updatable via API
      
      - project_id
          * ID of the project this contact belongs to
          * Read-only
    """

    def isInGroup(self, group):
        """
        Returns true if this contact is in a particular group, false otherwise.
        
        Arguments:
          - group (Group)
              * Required
          
        Returns:
            bool
        """
        self.load()
        return group.id in self._group_ids_set

    def addToGroup(self, group):
        """
        Adds this contact to a group.
        
        Arguments:
          - group (Group)
              * Required
        """

        self._api.doRequest("PUT", group.getBaseApiPath() + "/contacts/" + self.id);
        self._group_ids_set[group.id] = True

    def removeFromGroup(self, group):
        """
        Removes this contact from a group.
        
        Arguments:
          - group (Group)
              * Required
        """

        self._api.doRequest("DELETE", group.getBaseApiPath() + "/contacts/" + self.id)
        if group.id in self._group_ids_set:
            del self._group_ids_set[group.id]

    def queryMessages(self, **options):
        """
        Queries messages sent or received by this contact.
        
        Arguments:
            
            - direction
                * Filter messages by direction
                * Allowed values: incoming, outgoing
            
            - message_type
                * Filter messages by message_type
                * Allowed values: sms, mms, ussd, call, service
            
            - source
                * Filter messages by source
                * Allowed values: phone, provider, web, api, service, webhook, scheduled,
                    integration
            
            - starred (bool)
                * Filter messages by starred/unstarred
            
            - status
                * Filter messages by status
                * Allowed values: ignored, processing, received, sent, queued, failed,
                    failed_queued, cancelled, delivered, not_delivered, read
            
            - time_created[min] (UNIX timestamp)
                * Filter messages created on or after a particular time
            
            - time_created[max] (UNIX timestamp)
                * Filter messages created before a particular time
            
            - external_id
                * Filter messages by ID from an external provider
                * Allowed modifiers: external_id[ne], external_id[exists]
            
            - contact_id
                * ID of the contact who sent/received the message
                * Allowed modifiers: contact_id[ne], contact_id[exists]
            
            - phone_id
                * ID of the phone (basic route) that sent/received the message
            
            - broadcast_id
                * ID of the broadcast containing the message
                * Allowed modifiers: broadcast_id[ne], broadcast_id[exists]
            
            - scheduled_id
                * ID of the scheduled message that created this message
                * Allowed modifiers: scheduled_id[ne], scheduled_id[exists]
            
            - group_id
                * Filter messages sent or received by contacts in a particular group. The group must
                    be a normal group, not a dynamic group.
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Message)
        """
        from .message import Message
        return self._api.newApiCursor(Message, self.getBaseApiPath() + "/messages", options)

    def queryGroups(self, **options):
        """
        Queries groups for which this contact is a member.
        
        Arguments:
            
            - name
                * Filter groups by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - dynamic (bool)
                * Filter groups by dynamic/non-dynamic
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Group)
        """
        from .group import Group
        return self._api.newApiCursor(Group, self.getBaseApiPath() + "/groups", options)

    def queryScheduledMessages(self, **options):
        """
        Queries messages scheduled to this contact (not including messages scheduled to groups that
        this contact is a member of)
        
        Arguments:
            
            - message_type
                * Filter scheduled messages by message_type
                * Allowed values: sms, mms, ussd, call, service
            
            - time_created (UNIX timestamp)
                * Filter scheduled messages by time_created
                * Allowed modifiers: time_created[min], time_created[max]
            
            - next_time (UNIX timestamp)
                * Filter scheduled messages by next_time
                * Allowed modifiers: next_time[min], next_time[max], next_time[exists]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, next_time
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of ScheduledMessage)
        """
        from .scheduledmessage import ScheduledMessage
        return self._api.newApiCursor(ScheduledMessage, self.getBaseApiPath() + "/scheduled", options)

    def queryDataRows(self, **options):
        """
        Queries data rows associated with this contact (in any data table).
        
        Arguments:
            
            - time_created (UNIX timestamp)
                * Filter data rows by the time they were created
                * Allowed modifiers: time_created[min], time_created[max]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of DataRow)
        """
        from .datarow import DataRow
        return self._api.newApiCursor(DataRow, self.getBaseApiPath() + "/rows", options)

    def queryServiceStates(self, **options):
        """
        Queries this contact's current states for any service
        
        Arguments:
            
            - id
                * Filter states by id
                * Allowed modifiers: id[ne], id[prefix], id[not_prefix], id[gte], id[gt], id[lt],
                    id[lte]
            
            - vars (dict)
                * Filter states by value of a custom variable (e.g. vars[email], vars[foo], etc.)
                * Allowed modifiers: vars[foo][ne], vars[foo][prefix], vars[foo][not_prefix],
                    vars[foo][gte], vars[foo][gt], vars[foo][lt], vars[foo][lte], vars[foo][min],
                    vars[foo][max], vars[foo][exists]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of ContactServiceState)
        """
        from .contactservicestate import ContactServiceState
        return self._api.newApiCursor(ContactServiceState, self.getBaseApiPath() + "/states", options)

    def save(self):
        """
        Saves any fields or custom variables that have changed for this contact.
        """
        super(Contact, self).save()

    def delete(self):
        """
        Deletes this contact.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/contacts/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
    def _setData(self, data):
        super(Contact, self)._setData(data)

        self._group_ids_set = {}

        if 'group_ids' in data:
            for group_id in data['group_ids']:
                self._group_ids_set[group_id] = True
