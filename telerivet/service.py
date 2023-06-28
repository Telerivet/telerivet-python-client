
from .entity import Entity
        
class Service(Entity):
    """
    Represents an automated service on Telerivet, for example a poll, auto-reply, webhook
    service, etc.
    
    A service, generally, defines some automated behavior that can be
    invoked/triggered in a particular context, and may be invoked either manually or when a
    particular event occurs.
    
    Most commonly, services work in the context of a particular message, when
    the message is originally received by Telerivet.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the service
          * Read-only
      
      - name
          * Name of the service
          * Updatable via API
      
      - service_type
          * Type of the service.
          * Read-only
      
      - active (bool)
          * Whether the service is active or inactive. Inactive services are not automatically
              triggered and cannot be invoked via the API.
          * Updatable via API
      
      - priority (int)
          * A number that determines the order that services are triggered when a particular
              event occurs (smaller numbers are triggered first). Any service can determine whether
              or not execution "falls-through" to subsequent services (with larger priority values)
              by setting the return_value variable within Telerivet's Rules Engine.
          * Updatable via API
      
      - contexts (dict)
          * A key/value map where the keys are the names of contexts supported by this service
              (e.g. message, contact), and the values are themselves key/value maps where the keys
              are event names and the values are all true. (This structure makes it easy to test
              whether a service can be invoked for a particular context and event.)
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this service
          * Updatable via API
      
      - project_id
          * ID of the project this service belongs to
          * Read-only
      
      - response_table_id
          * ID of the data table where responses to this service will be stored
          * Updatable via API
      
      - phone_ids
          * IDs of phones (basic routes) associated with this service, or null if the service is
              associated with all routes. Only applies for service types that handle incoming
              messages, voice calls, or USSD sessions.
          * Updatable via API
      
      - apply_mode
          * If apply_mode is `unhandled`, the service will not be triggered if another service
              has already handled the incoming message. If apply_mode is `always`, the service will
              always be triggered regardless of other services. Only applies to services that handle
              incoming messages.
          * Allowed values: always, unhandled
          * Updatable via API
      
      - contact_number_filter
          * If contact_number_filter is `long_number`, this service will only be triggered if
              the contact phone number has at least 7 digits (ignoring messages from shortcodes and
              alphanumeric senders). If contact_number_filter is `all`, the service will be
              triggered for all contact phone numbers.  Only applies to services that handle
              incoming messages.
          * Allowed values: long_number, all
          * Updatable via API
      
      - show_action (bool)
          * Whether this service is shown in the 'Actions' menu within the Telerivet web app
              when the service is active. Only provided for service types that are manually
              triggered.
          * Updatable via API
      
      - direction
          * Determines whether the service handles incoming voice calls, outgoing voice calls,
              or both. Only applies to services that handle voice calls.
          * Allowed values: incoming, outgoing, both
          * Updatable via API
      
      - webhook_url
          * URL that a third-party can invoke to trigger this service. Only provided for
              services that are triggered by a webhook request.
          * Read-only
    """

    def invoke(self, **options):
        """
        Manually invoke this service in a particular context.
        
        For example, to send a poll to a particular contact (or resend the
        current question), you can invoke the poll service with context=contact, and `contact_id` as
        the ID of the contact to send the poll to. (To trigger a service to multiple contacts, use
        [project.sendBroadcast](#Project.sendBroadcast). To schedule a service in the future, use
        [project.scheduleMessage](#Project.scheduleMessage).)
        
        Or, to manually apply a service for an incoming message, you can
        invoke the service with `context`=`message`, `event`=`incoming_message`, and `message_id` as
        the ID of the incoming message. (This is normally not necessary, but could be used if you
        want to override Telerivet's standard priority-ordering of services.)
        
        Arguments:
              * Required
            
            - context
                * The name of the context in which this service is invoked
                * Allowed values: message, call, ussd_session, row, contact, project
                * Required
            
            - event
                * The name of the event that is triggered (must be supported by this service)
                * Default: default
            
            - message_id
                * The ID of the message this service is triggered for
                * Required if context is 'message'
            
            - contact_id
                * The ID of the contact this service is triggered for (either `contact_id` or
                    `phone_number` is required if `context` is 'contact')
            
            - phone_number
                * The phone number of the contact this service is triggered for (either `contact_id`
                    or `phone_number` is required if `context` is 'contact'). If no  contact exists with
                    this phone number, a new contact will be created.
            
            - variables (dict)
                * Object containing up to 25 temporary variable names and their corresponding values
                    to set when invoking the service. Values may be strings, numbers, or boolean
                    (true/false). String values may be up to 4096 bytes in length. Arrays and objects
                    are not supported. Within Custom Actions, each variable can be used like `[[$name]]`
                    (with a leading `$` character and surrounded by double square brackets). Within a
                    Cloud Script API service or JavaScript action, each variable will be available as a
                    global JavaScript variable like `$name` (with a leading `$` character).
            
            - route_id
                * The ID of the phone or route that the service will use for sending messages by
                    default
            
            - async (bool)
                * If set to true, the service will be invoked asynchronously. By default, queued
                    services will be invoked one at a time for each project.
          
        Returns:
            (associative array)
              - return_value (any)
                  * Return value of the service. May be any JSON type (boolean, number, string,
                      array, object, or null). (Undefined if async=true.)
              
              - log_entries (array)
                  * Array of log entry strings generated by the service. (Undefined if async=true.)
              
              - errors (array)
                  * Array of error message strings generated by the service. (Undefined if
                      async=true.)
              
              - sent_messages (array of objects)
                  * Array of messages sent by the service.
              
              - airtime_transactions (array of objects)
                  * Array of airtime transactions sent by the service (Undefined if async=true.)
        """
        
        invoke_result = self._api.doRequest('POST', self.getBaseApiPath() + '/invoke', options)
        
        if 'sent_messages' in invoke_result:
            from .message import Message
        
            sent_messages = []
            for sent_message_data in invoke_result['sent_messages']:
                sent_messages.append(Message(self._api, sent_message_data))
            
            invoke_result['sent_messages'] = sent_messages
            
        return invoke_result

    def getContactState(self, contact):
        """
        Gets the current state for a particular contact for this service.
        
        If the contact doesn't already have a state, this method will return
        a valid state object with id=null. However this object would not be returned by
        queryContactStates() unless it is saved with a non-null state id.
        
        Arguments:
          - contact (Contact)
              * The contact whose state you want to retrieve.
              * Required
          
        Returns:
            ContactServiceState
        """    
        from .contactservicestate import ContactServiceState
        return ContactServiceState(self._api, self._api.doRequest('GET', self.getBaseApiPath() + '/states/' + contact.id))
        
    def setContactState(self, contact, **options):
        """
        Initializes or updates the current state for a particular contact for the given service. If
        the state id is null, the contact's state will be reset.
        
        Arguments:
          - contact (Contact)
              * The contact whose state you want to update.
              * Required
          
              * Required
            
            - id (string, max 63 characters)
                * Arbitrary string representing the contact's current state for this service, e.g.
                    'q1', 'q2', etc.
                * Required
            
            - vars (dict)
                * Custom variables stored for this contact's state
          
        Returns:
            ContactServiceState
        """
        from .contactservicestate import ContactServiceState
        return ContactServiceState(self._api, self._api.doRequest('POST', self.getBaseApiPath() + '/states/' + contact.id, options))        
    
    def resetContactState(self, contact):
        """
        Resets the current state for a particular contact for the given service.
        
        Arguments:
          - contact (Contact)
              * The contact whose state you want to reset.
              * Required
          
        Returns:
            ContactServiceState
        """
        from .contactservicestate import ContactServiceState
        return ContactServiceState(self._api, self._api.doRequest('DELETE', self.getBaseApiPath() + '/states/' + contact.id))

    def queryContactStates(self, **options):
        """
        Query the current states of contacts for this service.
        
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

    def getConfig(self):
        """
        Gets configuration specific to the type of automated service.
        
        Only certain types of services provide their configuration via the
        API.
        
        Returns:
            object
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/config")

    def setConfig(self, **options):
        """
        Updates configuration specific to the type of automated service.
        
        Only certain types of services support updating their configuration
        via the API.
        
        Note: when updating a service of type custom_template_instance,
        the validation script will be invoked when calling this method.
        
        Arguments:
              * Required
          
        Returns:
            object
        """
        return self._api.doRequest("POST", self.getBaseApiPath() + "/config", options)

    def save(self):
        """
        Saves any fields or custom variables that have changed for this service.
        """
        super(Service, self).save()

    def delete(self):
        """
        Deletes this service.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/services/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
