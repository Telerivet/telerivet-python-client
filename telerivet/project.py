
from .entity import Entity

class Project(Entity):
    """
    Represents a Telerivet project.
    
    Provides methods for sending and scheduling messages, as well as
    accessing, creating and updating a variety of entities, including contacts, messages,
    scheduled messages, groups, labels, phones, services, and data tables.
    
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
      
      - url_slug
          * Unique string used as a component of the project's URL in the Telerivet web app
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this project
          * Updatable via API
      
      - organization_id (string, max 34 characters)
          * ID of the organization this project belongs to
          * Read-only
    """

    def sendMessage(self, **options):
        """
        Sends one message (SMS, MMS, voice call, or USSD request).
        
        Arguments:
              * Required
            
            - message_type
                * Type of message to send. If `text`, will use the default text message type for the
                    selected route.
                * Allowed values: sms, mms, ussd, call, text
                * Default: text
            
            - content
                * Content of the message to send (if `message_type` is `call`, the text will be
                    spoken during a text-to-speech call)
                * Required if sending SMS message
            
            - to_number (string)
                * Phone number to send the message to
                * Required if contact_id not set
            
            - contact_id
                * ID of the contact to send the message to
                * Required if to_number not set
            
            - route_id
                * ID of the phone or route to send the message from
                * Default: default sender route ID for your project
            
            - status_url
                * Webhook callback URL to be notified when message status changes
            
            - status_secret
                * POST parameter 'secret' passed to status_url
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content. [(See
                    available variables)](#variables)
                * Default: false
            
            - track_clicks (boolean)
                * If true, URLs in the message content will automatically be replaced with unique
                    short URLs.
                * Default: false
            
            - media_urls (array)
                * URLs of media files to attach to the text message. If `message_type` is `sms`,
                    short links to each media URL will be appended to the end of the content (separated
                    by a new line).
            
            - label_ids (array)
                * List of IDs of labels to add to this message
            
            - vars (dict)
                * Custom variables to store with the message
            
            - priority (int)
                * Priority of the message. Telerivet will attempt to send messages with higher
                    priority numbers first (for example, so you can prioritize an auto-reply ahead of a
                    bulk message to a large group).
                * Allowed values: 1, 2
                * Default: 1
            
            - simulated (bool)
                * Set to true to test the Telerivet API without actually sending a message from the
                    route
                * Default: false
            
            - service_id
                * Service that defines the call flow of the voice call (when `message_type` is
                    `call`)
            
            - audio_url
                * The URL of an MP3 file to play when the contact answers the call (when
                    `message_type` is `call`).
                    
                    If `audio_url` is provided, the text-to-speech voice is not used to say
                    `content`, although you can optionally use `content` to indicate the script for the
                    audio.
                    
                    For best results, use an MP3 file containing only speech. Music is not
                    recommended because the audio quality will be low when played over a phone line.
            
            - tts_lang
                * The language of the text-to-speech voice (when `message_type` is `call`)
                * Allowed values: en-US, en-GB, en-GB-WLS, en-AU, en-IN, da-DK, nl-NL, fr-FR, fr-CA,
                    de-DE, is-IS, it-IT, pl-PL, pt-BR, pt-PT, ru-RU, es-ES, es-US, sv-SE
                * Default: en-US
            
            - tts_voice
                * The name of the text-to-speech voice (when message_type=call)
                * Allowed values: female, male
                * Default: female
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/messages/send", options))

    def sendBroadcast(self, **options):
        """
        Sends a text message (optionally with mail-merge templates) or voice call to a group or a
        list of up to 500 phone numbers.
        
        With `message_type`=`service`, invokes an automated service (such as
        a poll) for a group or list of phone numbers. Any service that can be triggered for a
        contact can be invoked via this method, whether or not the service actually sends a message.
        
        Arguments:
              * Required
            
            - message_type
                * Type of message to send. If `text`, will use the default text message type for the
                    selected route.
                * Allowed values: sms, mms, call, service, text
                * Default: text
            
            - content
                * Content of the message to send
                * Required if sending SMS message
            
            - group_id
                * ID of the group to send the message to
                * Required if to_numbers not set
            
            - to_numbers (array of strings)
                * List of up to 500 phone numbers to send the message to
                * Required if group_id not set
            
            - route_id
                * ID of the phone or route to send the message from
                * Default: default sender route ID
            
            - title (string)
                * Title of the broadcast. If a title is not provided, a title will automatically be
                    generated from the recipient group name or phone numbers.
            
            - status_url
                * Webhook callback URL to be notified when message status changes
            
            - status_secret
                * POST parameter 'secret' passed to status_url
            
            - label_ids (array)
                * Array of IDs of labels to add to all messages sent (maximum 5). Does not apply
                    when `message_type`=`service`, since the labels are determined by the service
                    itself.
            
            - exclude_contact_id
                * Optionally excludes one contact from receiving the message (only when group_id is
                    set)
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content [(See
                    available variables)](#variables)
                * Default: false
            
            - track_clicks (boolean)
                * If true, URLs in the message content will automatically be replaced with unique
                    short URLs.
                * Default: false
            
            - media_urls (array)
                * URLs of media files to attach to the text message. If `message_type` is `sms`,
                    short links to each URL will be appended to the end of the content (separated by a
                    new line).
            
            - vars (dict)
                * Custom variables to set for each message
            
            - service_id
                * Service to invoke for each recipient (when `message_type` is `call` or `service`)
                * Required if message_type is service
            
            - audio_url
                * The URL of an MP3 file to play when the contact answers the call (when
                    `message_type` is `call`).
                    
                    If `audio_url` is provided, the text-to-speech voice is not used to say
                    `content`, although you can optionally use `content` to indicate the script for the
                    audio.
                    
                    For best results, use an MP3 file containing only speech. Music is not
                    recommended because the audio quality will be low when played over a phone line.
            
            - tts_lang
                * The language of the text-to-speech voice (when `message_type` is `call`)
                * Allowed values: en-US, en-GB, en-GB-WLS, en-AU, en-IN, da-DK, nl-NL, fr-FR, fr-CA,
                    de-DE, is-IS, it-IT, pl-PL, pt-BR, pt-PT, ru-RU, es-ES, es-US, sv-SE
                * Default: en-US
            
            - tts_voice
                * The name of the text-to-speech voice (when message_type=call)
                * Allowed values: female, male
                * Default: female
          
        Returns:
            Broadcast
        """
        from .broadcast import Broadcast
        return Broadcast(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/send_broadcast", options))

    def sendMulti(self, **options):
        """
        Sends up to 100 different messages in a single API request. This method is significantly
        faster than sending a separate API request for each message.
        
        Arguments:
              * Required
            
            - messages (array)
                * Array of up to 100 objects with `content` and `to_number` properties. Each object
                    may also contain the optional properties `status_url`, `status_secret`, `vars`,
                    and/or `priority`, which override the parameters of the same name defined below, to
                    allow passing different values for each message.
                * Required
            
            - message_type
                * Type of message to send. If `text`, will use the default text message type for the
                    selected route.
                * Allowed values: sms, mms, chat, text
                * Default: text
            
            - route_id
                * ID of the phone or route to send the messages from
                * Default: default sender route ID
            
            - broadcast_id (string)
                * ID of an existing broadcast to associate the messages with
            
            - broadcast_title (string)
                * Title of broadcast to create (when `broadcast_id` is not provided).
                    When sending more than 100 messages over multiple API
                    requests, you can associate all messages with the same broadcast by providing a
                    `broadcast_title` parameter in the first
                    API request, then retrieving the `broadcast_id` property
                    from the API response, and passing it as the `broadcast_id` parameter in subsequent
                    API requests.
            
            - status_url
                * Webhook callback URL to be notified when message status changes
            
            - status_secret
                * POST parameter 'secret' passed to status_url
            
            - label_ids (array)
                * Array of IDs of labels to add to each message (maximum 5)
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content [(See
                    available variables)](#variables)
                * Default: false
            
            - media_urls (array)
                * URLs of media files to attach to the text message. If `message_type` is `sms`,
                    short links to each media URL will be appended to the end of the content (separated
                    by a new line).
            
            - vars (dict)
                * Custom variables to store with the message
            
            - priority (int)
                * Priority of the message. Telerivet will attempt to send messages with higher
                    priority numbers first (for example, so you can prioritize an auto-reply ahead of a
                    bulk message to a large group).
                * Allowed values: 1, 2
                * Default: 1
            
            - simulated (bool)
                * Set to true to test the Telerivet API without actually sending a message from the
                    route
                * Default: false
          
        Returns:
            (associative array)
              - messages (array)
                  * List of objects representing each newly created message, with the same length
                      and order as provided in the `messages` parameter in the API request.
                      Each object has the `id` and `status` properties,
                      and may have the property `error_message`.
                      (Other properties of the Message object are
                      omitted in order to reduce the amount of redundant data sent in each API
                      response.)
              
              - broadcast_id
                  * ID of broadcast that these messages are associated with, if `broadcast_id` or
                      `broadcast_title` parameter is provided in the API request.
        """
        data = self._api.doRequest("POST", self.getBaseApiPath() + "/send_multi", options)
        return data

    def sendMessages(self, **options):
        """
        (Deprecated) Send a message a to group or a list of phone numbers.
        This method is only needed to maintain backward compatibility with
        code developed using previous versions of the client library.
        Use `sendBroadcast` or `sendMulti` instead.
        
        Arguments:
              * Required
            
            - message_type
            
            - content
                * Required
            
            - group_id
            
            - to_numbers
          
        Returns:
            (associative array)
              - count_queued (int)
                  * Number of messages queued to send
              
              - broadcast_id
                  * ID of broadcast created for this message batch.
        """
        data = self._api.doRequest("POST", self.getBaseApiPath() + "/messages/send_batch", options)
        return data

    def scheduleMessage(self, **options):
        """
        Schedules a message to a group or single contact. Note that Telerivet only sends scheduled
        messages approximately once every 15 seconds, so it is not possible to control the exact
        second at which a scheduled message is sent.
        
        With `message_type`=`service`, schedules an automated service (such
        as a poll) to be invoked for a group or list of phone numbers. Any service that can be
        triggered for a contact can be scheduled via this method, whether or not the service
        actually sends a message.
        
        Arguments:
              * Required
            
            - message_type
                * Type of message to send
                * Allowed values: sms, ussd, call, service
                * Default: sms
            
            - content
                * Content of the message to schedule
                * Required if sending SMS message
            
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
                    (UNTIL is ignored; use end_time parameter instead).
                * Default: COUNT=1 (one-time scheduled message, does not repeat)
            
            - route_id
                * ID of the phone or route to send the message from
                * Default: default sender route ID
            
            - service_id
                * Service to invoke for each recipient (when `message_type` is `call` or `service`)
                * Required if message_type is service
            
            - audio_url
                * The URL of an MP3 file to play when the contact answers the call (when
                    `message_type` is `call`).
                    
                    If `audio_url` is provided, the text-to-speech voice is not used to say
                    `content`, although you can optionally use `content` to indicate the script for the
                    audio.
                    
                    For best results, use an MP3 file containing only speech. Music is not
                    recommended because the audio quality will be low when played over a phone line.
            
            - tts_lang
                * The language of the text-to-speech voice (when `message_type` is `call`)
                * Allowed values: en-US, en-GB, en-GB-WLS, en-AU, en-IN, da-DK, nl-NL, fr-FR, fr-CA,
                    de-DE, is-IS, it-IT, pl-PL, pt-BR, pt-PT, ru-RU, es-ES, es-US, sv-SE
                * Default: en-US
            
            - tts_voice
                * The name of the text-to-speech voice (when message_type=call)
                * Allowed values: female, male
                * Default: female
            
            - track_clicks (boolean)
                * If true, URLs in the message content will automatically be replaced with unique
                    short URLs.
                * Default: false
            
            - is_template (bool)
                * Set to true to evaluate variables like [[contact.name]] in message content
                * Default: false
            
            - media_urls (array)
                * URLs of media files to attach to the text message. If `message_type` is `sms`,
                    short links to each media URL will be appended to the end of the content (separated
                    by a new line).
            
            - label_ids (array)
                * Array of IDs of labels to add to the sent messages (maximum 5). Does not apply
                    when `message_type`=`service`, since the labels are determined by the service
                    itself.
            
            - timezone_id
                * TZ database timezone ID; see
                    <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>
                * Default: project default timezone
            
            - end_time (UNIX timestamp)
                * Time after which a recurring message will stop (not applicable to non-recurring
                    scheduled messages)
            
            - end_time_offset (int)
                * Number of seconds from now until the recurring message will stop
            
            - vars (dict)
                * Custom variables to set for this scheduled message, which will be copied to each
                    message sent from this scheduled message
          
        Returns:
            ScheduledMessage
        """
        from .scheduledmessage import ScheduledMessage
        return ScheduledMessage(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/scheduled", options))

    def receiveMessage(self, **options):
        """
        Add an incoming message to Telerivet. Acts the same as if the message was received by a
        phone. Also triggers any automated services that apply to the message.
        
        Arguments:
              * Required
            
            - content
                * Content of the incoming message
                * Required unless `message_type` is `call`
            
            - message_type
                * Type of message
                * Allowed values: sms, call
                * Default: sms
            
            - from_number
                * Phone number that sent the incoming message
                * Required
            
            - phone_id
                * ID of the phone (basic route) that received the message
                * Required
            
            - to_number
                * Phone number that the incoming message was sent to
                * Default: phone number of the phone that received the message
            
            - simulated (bool)
                * If true, Telerivet will not send automated replies to actual phones
            
            - starred (bool)
                * True if this message should be starred
            
            - label_ids (array)
                * Array of IDs of labels to add to this message (maximum 5)
            
            - vars (dict)
                * Custom variables to set for this message
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/messages/receive", options))

    def getOrCreateContact(self, **options):
        """
        Retrieves OR creates and possibly updates a contact by name or phone number.
        
        If a phone number is provided, by default, Telerivet will search for
        an existing contact with that phone number (including suffix matches to allow finding
        contacts with phone numbers in a different format). If a phone number is not provided but a
        name is provided, Telerivet will search for a contact with that exact name (case
        insensitive). This behavior can be modified by setting the `lookup_key` parameter to look up
        a contact by another field, including a custom variable.
        
        If no existing contact is found, a new contact will be created.
        
        Then that contact will be updated with any parameters provided
        (`name`, `phone_number`, `vars`, `default_route_id`, `send_blocked`, `add_group_ids`,
        `remove_group_ids`).
        
        Arguments:
            
            - name
                * Name of the contact
            
            - phone_number
                * Phone number of the contact
            
            - lookup_key
                * The field used to search for a matching contact, or 'none' to always create a new
                    contact. To search by a custom variable, precede the variable name with 'vars.'.
                * Allowed values: phone_number, name, id, vars.variable_name, none
                * Default: phone_number
            
            - send_blocked (bool)
                * True if Telerivet is blocked from sending messages to this contact
            
            - default_route_id
                * ID of the route to use by default to send messages to this contact
            
            - add_group_ids (array)
                * ID of one or more groups to add this contact as a member (max 20)
            
            - id
                * ID of an existing contact (only used if `lookup_key` is 'id')
            
            - remove_group_ids (array)
                * ID of one or more groups to remove this contact as a member (max 20)
            
            - vars (dict)
                * Custom variables and values to update on the contact
          
        Returns:
            Contact
        """
        from .contact import Contact
        return Contact(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/contacts", options))

    def importContacts(self, **options):
        """
        Creates and/or updates up to 200 contacts in a single API call. When creating or updating a
        large number of contacts, this method is significantly faster than sending a separate API
        request for each contact.
        
        By default, if the phone number for any contact matches an existing
        contact, the existing contact will be updated with any information provided. This behavior
        can be modified by setting the `lookup_key` parameter to look up contacts by another field,
        including a custom variable.
        
        If any contact was not found matching the provided `lookup_key`, a
        new contact will be created.
        
        Arguments:
              * Required
            
            - contacts (array)
                * Array of up to 200 objects which may contain the properties `name` (string),
                    `phone_number` (string), `vars` (object), and `send_blocked` (boolean). All
                    properties are optional, unless used as a lookup key; however, either a `name` or
                    `phone_number` property must be provided for new contacts.
                * Required
            
            - lookup_key
                * The field used to search for a matching contact, or 'none' to always create a new
                    contact. To search by a custom variable, precede the variable name with 'vars.'.
                * Allowed values: phone_number, id, vars.variable_name, none
                * Default: phone_number
            
            - add_group_ids (array)
                * ID of one or more groups to add these contacts as members (max 5)
            
            - remove_group_ids (array)
                * ID of one or more groups to remove these contacts as members (max 5)
            
            - default_route_id
                * ID of the route to use by default to send messages to these contacts
          
        Returns:
            (associative array)
              - contacts (array)
                  * List of objects representing each contact, with the same length and order as
                      provided in the `contacts` parameter in the API request. Each object has a string
                      `id` property.
        """
        data = self._api.doRequest("POST", self.getBaseApiPath() + "/import_contacts", options)
        return data

    def queryContacts(self, **options):
        """
        Queries contacts within the given project.
        
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
            
            - last_incoming_message_time (UNIX timestamp)
                * Filter contacts by last time a message was received
                * Allowed modifiers: last_incoming_message_time[exists],
                    last_incoming_message_time[ne], last_incoming_message_time[min],
                    last_incoming_message_time[max]
            
            - last_outgoing_message_time (UNIX timestamp)
                * Filter contacts by last time a message was sent
                * Allowed modifiers: last_outgoing_message_time[exists],
                    last_outgoing_message_time[ne], last_outgoing_message_time[min],
                    last_outgoing_message_time[max]
            
            - incoming_message_count (int)
                * Filter contacts by number of messages received from the contact
                * Allowed modifiers: incoming_message_count[ne], incoming_message_count[min],
                    incoming_message_count[max]
            
            - outgoing_message_count (int)
                * Filter contacts by number of messages sent to the contact
                * Allowed modifiers: outgoing_message_count[ne], outgoing_message_count[min],
                    outgoing_message_count[max]
            
            - send_blocked (bool)
                * Filter contacts by blocked status
            
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
                * Number of results returned per page (max 500)
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
        Retrieves the contact with the given ID.
        
        Arguments:
          - id
              * ID of the contact
              * Required
          
        Returns:
            Contact
        """
        from .contact import Contact
        return Contact(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/contacts/%s" % (id)))

    def initContactById(self, id):
        """
        Initializes the Telerivet contact with the given ID without making an API request.
        
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
        Queries phones within the given project.
        
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
                * Number of results returned per page (max 500)
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
        Retrieves the phone with the given ID.
        
        Arguments:
          - id
              * ID of the phone - see <https://telerivet.com/dashboard/api>
              * Required
          
        Returns:
            Phone
        """
        from .phone import Phone
        return Phone(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/phones/%s" % (id)))

    def initPhoneById(self, id):
        """
        Initializes the phone with the given ID without making an API request.
        
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
        Queries messages within the given project.
        
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
                    failed_queued, cancelled, delivered, not_delivered
            
            - time_created[min] (UNIX timestamp)
                * Filter messages created on or after a particular time
            
            - time_created[max] (UNIX timestamp)
                * Filter messages created before a particular time
            
            - external_id
                * Filter messages by ID from an external provider
            
            - contact_id
                * ID of the contact who sent/received the message
            
            - phone_id
                * ID of the phone (basic route) that sent/received the message
            
            - broadcast_id
                * ID of the broadcast containing the message
            
            - scheduled_id
                * ID of the scheduled message that created this message
            
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

    def getMessageById(self, id):
        """
        Retrieves the message with the given ID.
        
        Arguments:
          - id
              * ID of the message
              * Required
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/messages/%s" % (id)))

    def initMessageById(self, id):
        """
        Initializes the Telerivet message with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the message
              * Required
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, {'project_id': self.id, 'id': id}, False)

    def queryBroadcasts(self, **options):
        """
        Queries broadcasts within the given project.
        
        Arguments:
            
            - time_created[min] (UNIX timestamp)
                * Filter broadcasts created on or after a particular time
            
            - time_created[max] (UNIX timestamp)
                * Filter broadcasts created before a particular time
            
            - last_message_time[min] (UNIX timestamp)
                * Filter broadcasts with most recent message on or after a particular time
            
            - last_message_time[max] (UNIX timestamp)
                * Filter broadcasts with most recent message before a particular time
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, last_message_time
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
            APICursor (of Broadcast)
        """
        from .broadcast import Broadcast
        return self._api.newApiCursor(Broadcast, self.getBaseApiPath() + "/broadcasts", options)

    def getBroadcastById(self, id):
        """
        Retrieves the broadcast with the given ID.
        
        Arguments:
          - id
              * ID of the broadcast
              * Required
          
        Returns:
            Broadcast
        """
        from .broadcast import Broadcast
        return Broadcast(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/broadcasts/%s" % (id)))

    def initBroadcastById(self, id):
        """
        Initializes the Telerivet broadcast with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the broadcast
              * Required
          
        Returns:
            Broadcast
        """
        from .broadcast import Broadcast
        return Broadcast(self._api, {'project_id': self.id, 'id': id}, False)

    def queryGroups(self, **options):
        """
        Queries groups within the given project.
        
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

    def getOrCreateGroup(self, name):
        """
        Retrieves or creates a group by name.
        
        Arguments:
          - name
              * Name of the group
              * Required
          
        Returns:
            Group
        """
        from .group import Group
        return Group(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/groups", {'name': name}))

    def getGroupById(self, id):
        """
        Retrieves the group with the given ID.
        
        Arguments:
          - id
              * ID of the group
              * Required
          
        Returns:
            Group
        """
        from .group import Group
        return Group(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/groups/%s" % (id)))

    def initGroupById(self, id):
        """
        Initializes the group with the given ID without making an API request.
        
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
        Queries labels within the given project.
        
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
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Label)
        """
        from .label import Label
        return self._api.newApiCursor(Label, self.getBaseApiPath() + "/labels", options)

    def getOrCreateLabel(self, name):
        """
        Gets or creates a label by name.
        
        Arguments:
          - name
              * Name of the label
              * Required
          
        Returns:
            Label
        """
        from .label import Label
        return Label(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/labels", {'name': name}))

    def getLabelById(self, id):
        """
        Retrieves the label with the given ID.
        
        Arguments:
          - id
              * ID of the label
              * Required
          
        Returns:
            Label
        """
        from .label import Label
        return Label(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/labels/%s" % (id)))

    def initLabelById(self, id):
        """
        Initializes the label with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the label
              * Required
          
        Returns:
            Label
        """
        from .label import Label
        return Label(self._api, {'project_id': self.id, 'id': id}, False)

    def queryDataTables(self, **options):
        """
        Queries data tables within the given project.
        
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
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of DataTable)
        """
        from .datatable import DataTable
        return self._api.newApiCursor(DataTable, self.getBaseApiPath() + "/tables", options)

    def getOrCreateDataTable(self, name):
        """
        Gets or creates a data table by name.
        
        Arguments:
          - name
              * Name of the data table
              * Required
          
        Returns:
            DataTable
        """
        from .datatable import DataTable
        return DataTable(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/tables", {'name': name}))

    def getDataTableById(self, id):
        """
        Retrieves the data table with the given ID.
        
        Arguments:
          - id
              * ID of the data table
              * Required
          
        Returns:
            DataTable
        """
        from .datatable import DataTable
        return DataTable(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/tables/%s" % (id)))

    def initDataTableById(self, id):
        """
        Initializes the data table with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the data table
              * Required
          
        Returns:
            DataTable
        """
        from .datatable import DataTable
        return DataTable(self._api, {'project_id': self.id, 'id': id}, False)

    def queryScheduledMessages(self, **options):
        """
        Queries scheduled messages within the given project.
        
        Arguments:
            
            - message_type
                * Filter scheduled messages by message_type
                * Allowed values: sms, mms, ussd, call, service
            
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

    def getScheduledMessageById(self, id):
        """
        Retrieves the scheduled message with the given ID.
        
        Arguments:
          - id
              * ID of the scheduled message
              * Required
          
        Returns:
            ScheduledMessage
        """
        from .scheduledmessage import ScheduledMessage
        return ScheduledMessage(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/scheduled/%s" % (id)))

    def initScheduledMessageById(self, id):
        """
        Initializes the scheduled message with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the scheduled message
              * Required
          
        Returns:
            ScheduledMessage
        """
        from .scheduledmessage import ScheduledMessage
        return ScheduledMessage(self._api, {'project_id': self.id, 'id': id}, False)

    def queryServices(self, **options):
        """
        Queries services within the given project.
        
        Arguments:
            
            - name
                * Filter services by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - active (bool)
                * Filter services by active/inactive state
            
            - context
                * Filter services that can be invoked in a particular context
                * Allowed values: message, call, contact, project
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, priority, name
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
            APICursor (of Service)
        """
        from .service import Service
        return self._api.newApiCursor(Service, self.getBaseApiPath() + "/services", options)

    def getServiceById(self, id):
        """
        Retrieves the service with the given ID.
        
        Arguments:
          - id
              * ID of the service
              * Required
          
        Returns:
            Service
        """
        from .service import Service
        return Service(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/services/%s" % (id)))

    def initServiceById(self, id):
        """
        Initializes the service with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the service
              * Required
          
        Returns:
            Service
        """
        from .service import Service
        return Service(self._api, {'project_id': self.id, 'id': id}, False)

    def queryRoutes(self, **options):
        """
        Queries custom routes that can be used to send messages (not including Phones).
        
        Arguments:
            
            - name
                * Filter routes by name
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
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Route)
        """
        from .route import Route
        return self._api.newApiCursor(Route, self.getBaseApiPath() + "/routes", options)

    def getRouteById(self, id):
        """
        Gets a custom route by ID
        
        Arguments:
          - id
              * ID of the route
              * Required
          
        Returns:
            Route
        """
        from .route import Route
        return Route(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/routes/%s" % (id)))

    def initRouteById(self, id):
        """
        Initializes a custom route by ID without making an API request.
        
        Arguments:
          - id
              * ID of the route
              * Required
          
        Returns:
            Route
        """
        from .route import Route
        return Route(self._api, {'project_id': self.id, 'id': id}, False)

    def getUsers(self):
        """
        Returns an array of user accounts that have access to this project. Each item in the array
        is an object containing `id`, `email`, and `name` properties. (The id corresponds to the
        `user_id` property of the Message object.)
        
        Returns:
            array
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/users")

    def queryAirtimeTransactions(self, **options):
        """
        Returns information about each airtime transaction.
        
        Arguments:
            
            - time_created[min] (UNIX timestamp)
                * Filter transactions created on or after a particular time
            
            - time_created[max] (UNIX timestamp)
                * Filter transactions created before a particular time
            
            - contact_id
                * Filter transactions sent to a particular contact
            
            - to_number
                * Filter transactions sent to a particular phone number
            
            - service_id
                * Filter transactions sent by a particular service
            
            - status
                * Filter transactions by status
                * Allowed values: pending, queued, processing, successful, failed, cancelled,
                    pending_payment, pending_approval
            
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
            APICursor (of AirtimeTransaction)
        """
        from .airtimetransaction import AirtimeTransaction
        return self._api.newApiCursor(AirtimeTransaction, self.getBaseApiPath() + "/airtime_transactions", options)

    def getAirtimeTransactionById(self, id):
        """
        Gets an airtime transaction by ID
        
        Arguments:
          - id
              * ID of the airtime transaction
              * Required
          
        Returns:
            AirtimeTransaction
        """
        from .airtimetransaction import AirtimeTransaction
        return AirtimeTransaction(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/airtime_transactions/%s" % (id)))

    def initAirtimeTransactionById(self, id):
        """
        Initializes an airtime transaction by ID without making an API request.
        
        Arguments:
          - id
              * ID of the airtime transaction
              * Required
          
        Returns:
            AirtimeTransaction
        """
        from .airtimetransaction import AirtimeTransaction
        return AirtimeTransaction(self._api, {'project_id': self.id, 'id': id}, False)

    def save(self):
        """
        Saves any fields or custom variables that have changed for the project.
        """
        super(Project, self).save()

    def getBaseApiPath(self):
        return "/projects/%(id)s" % {'id': self.id} 
