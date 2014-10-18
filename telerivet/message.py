from .entity import Entity

class Message(Entity):    
    """
    Represents a single message.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the message
          * Read-only
      
      - direction
          * Direction of the message: incoming messages are sent from one of your contacts to
              your phone; outgoing messages are sent from your phone to one of your contacts
          * Allowed values: incoming, outgoing
          * Read-only
      
      - status
          * Current status of the message
          * Allowed values: ignored, processing, received, sent, queued, failed, failed_queued,
              cancelled, delivered, not_delivered
          * Read-only
      
      - message_type
          * Type of the message
          * Allowed values: sms, mms, ussd, call
          * Read-only
      
      - source
          * How the message originated within Telerivet
          * Allowed values: phone, provider, web, api, service, webhook, scheduled
          * Read-only
      
      - time_created (UNIX timestamp)
          * The time that the message was created on Telerivet's servers
          * Read-only
      
      - time_sent (UNIX timestamp)
          * The time that the message was reported to have been sent (null for incoming messages
              and messages that have not yet been sent)
          * Read-only
      
      - from_number (string)
          * The phone number that the message originated from (your number for outgoing
              messages, the contact's number for incoming messages)
          * Read-only
      
      - to_number (string)
          * The phone number that the message was sent to (your number for incoming messages,
              the contact's number for outgoing messages)
          * Read-only
      
      - content (string)
          * The text content of the message (null for USSD messages and calls)
          * Read-only
      
      - starred (bool)
          * Whether this message is starred in Telerivet
          * Updatable via API
      
      - simulated (bool)
          * Whether this message is was simulated within Telerivet for testing (and not actually
              sent to or received by a real phone)
          * Read-only
      
      - label_ids (array)
          * List of IDs of labels applied to this message
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this message
          * Updatable via API
      
      - error_message
          * A description of the error encountered while sending a message. (This field is
              omitted from the API response if there is no error message.)
          * Updatable via API
      
      - external_id
          * The ID of this message from an external SMS gateway provider (e.g. Twilio or Nexmo),
              if available.
          * Read-only
      
      - price (number)
          * The price of this message, if known. By convention, message prices are negative.
          * Read-only
      
      - price_currency
          * The currency of the message price, if applicable.
          * Read-only
      
      - mms_parts (array)
          * A list of parts in the MMS message, the same as returned by the
              [getMMSParts](#Message.getMMSParts) method.
              
              Note: This property is only present when retrieving an individual
              MMS message by ID, not when querying a list of messages. In other cases, use
              [getMMSParts](#Message.getMMSParts).
          * Read-only
      
      - phone_id (string, max 34 characters)
          * ID of the phone that sent or received the message
          * Read-only
      
      - contact_id (string, max 34 characters)
          * ID of the contact that sent or received the message
          * Read-only
      
      - project_id
          * ID of the project this contact belongs to
          * Read-only
    """

    def hasLabel(self, label):
        """
        Returns true if this message has a particular label, false otherwise.
        
        Arguments:
          - label (Label)
              * Required
          
        Returns:
            bool
        """
    
        self.load()
        return label.id in self._label_ids_set
      
    def addLabel(self, label):
        """
        Adds a label to the given message.
        
        Arguments:
          - label (Label)
              * Required
        """
        
        self._api.doRequest("PUT", label.getBaseApiPath() + "/messages/" + self.id);
        self._label_ids_set[label.id] = True
    
    def removeLabel(self, label):
        """
        Removes a label from the given message.
        
        Arguments:
          - label (Label)
              * Required
        """
    
        self._api.doRequest("DELETE", label.getBaseApiPath() + "/messages/" + self.id)
        if label.id in self._label_ids_set:
            del self._label_ids_set[label.id]

    def delete(self):    
        """
        Deletes this message.
        """
        
        self._api.doRequest("DELETE", self.getBaseApiPath())

    #def getBaseApiPath(self):
    #    return "/projects/" + self.project_id + "/messages/" + self.id
        
    def getMMSParts(self):
        """
        Retrieves a list of MMS parts for this message (empty for non-MMS messages).
        
        Each MMS part in the list is an object with the following
        properties:
        
        - cid: MMS content-id
        - type: MIME type
        - filename: original filename
        - size (int): number of bytes
        - url: URL where the content for this part is stored (secret but
        publicly accessible, so you could link/embed it in a web page without having to re-host it
        yourself)
        
        Returns:
            array
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/mms_parts")

    def save(self):
        """
        Saves any fields that have changed for this message.
        """
        super(Message, self).save()

    def resend(self):
        """
        Resends a message, for example if the message failed to send or if it was not delivered. If
        the message was originally in the queued, retrying, failed, or cancelled states, then
        Telerivet will return the same message object. Otherwise, Telerivet will create and return a
        new message object.
        
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/resend"))

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/messages/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
    
    def _setData(self, data):    
        super(Message, self)._setData(data)
        
        self._label_ids_set = {}
        
        if 'label_ids' in data:
            for label_id in data['label_ids']:            
                self._label_ids_set[label_id] = True
    