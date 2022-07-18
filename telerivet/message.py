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
              cancelled, delivered, not_delivered, read
          * Read-only
      
      - message_type
          * Type of the message
          * Allowed values: sms, mms, ussd, call, service
          * Read-only
      
      - source
          * How the message originated within Telerivet
          * Allowed values: phone, provider, web, api, service, webhook, scheduled, integration
          * Read-only
      
      - time_created (UNIX timestamp)
          * The time that the message was created on Telerivet's servers
          * Read-only
      
      - time_sent (UNIX timestamp)
          * The time that the message was reported to have been sent (null for incoming messages
              and messages that have not yet been sent)
          * Read-only
      
      - time_updated (UNIX timestamp)
          * The time that the message was last updated in Telerivet.
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
          * Whether this message was simulated within Telerivet for testing (and not actually
              sent to or received by a real phone)
          * Read-only
      
      - label_ids (array)
          * List of IDs of labels applied to this message
          * Read-only
      
      - route_params (dict)
          * Route-specific parameters for the message. The parameters object may have keys
              matching the `phone_type` field of a phone (basic route) that may be used to send the
              message. The corresponding value is an object with route-specific parameters to use
              when the message is sent by that type of route.
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this message
          * Updatable via API
      
      - priority (int)
          * Priority of this message. Telerivet will attempt to send messages with higher
              priority numbers first. Only defined for outgoing messages.
          * Read-only
      
      - error_message
          * A description of the error encountered while sending a message. (This field is
              omitted from the API response if there is no error message.)
          * Updatable via API
      
      - external_id
          * The ID of this message from an external SMS gateway provider (e.g. Twilio or Nexmo),
              if available.
          * Read-only
      
      - price (number)
          * The price of this message, if known.
          * Read-only
      
      - price_currency
          * The currency of the message price, if applicable.
          * Read-only
      
      - duration (number)
          * The duration of the call in seconds, if known, or -1 if the call was not answered.
          * Read-only
      
      - ring_time (number)
          * The length of time the call rang in seconds before being answered or hung up, if
              known.
          * Read-only
      
      - audio_url
          * For voice calls, the URL of an MP3 file to play when the contact answers the call
          * Read-only
      
      - tts_lang
          * For voice calls, the language of the text-to-speech voice
          * Allowed values: en-US, en-GB, en-GB-WLS, en-AU, en-IN, da-DK, nl-NL, fr-FR, fr-CA,
              de-DE, is-IS, it-IT, pl-PL, pt-BR, pt-PT, ru-RU, es-ES, es-US, sv-SE
          * Read-only
      
      - tts_voice
          * For voice calls, the text-to-speech voice
          * Allowed values: female, male
          * Read-only
      
      - track_clicks (boolean)
          * If true, URLs in the message content are short URLs that redirect to a destination
              URL.
          * Read-only
      
      - short_urls (array)
          * For text messages containing short URLs, this is an array of objects with the
              properties `short_url`, `link_type`, `time_clicked` (the first time that URL was
              clicked), and `expiration_time`. If `link_type` is "redirect", the object also
              contains a `destination_url` property. If `link_type` is "media", the object also
              contains an `media_index` property (the index in the media array). If `link_type` is
              "service", the object also contains a `service_id` property. This property is
              undefined for messages that do not contain short URLs.
          * Read-only
      
      - media (array)
          * For text messages containing media files, this is an array of objects with the
              properties `url`, `type` (MIME type), `filename`, and `size` (file size in bytes).
              Unknown properties are null. This property is undefined for messages that do not
              contain media files. Note: For files uploaded via the Telerivet web app, the URL is
              temporary and may not be valid for more than 1 day.
          * Read-only
      
      - mms_parts (array)
          * A list of parts in the MMS message (only for incoming MMS messages received via
              Telerivet Gateway Android app).
              
              Each MMS part in the list is an object with the following
              properties:
              
              - cid: MMS content-id
              - type: MIME type
              - filename: original filename
              - size (int): number of bytes
              - url: URL where the content for this part is stored (secret but
              publicly accessible, so you could link/embed it in a web page without having to
              re-host it yourself)
              
              In general, the `media` property of the message is recommended for
              retrieving information about MMS media files, instead of `mms_parts`.
              The `mms_parts` property is also only present when retrieving an
              individual MMS message by ID, not when querying a list of messages.
          * Read-only
      
      - time_clicked (UNIX timestamp)
          * If the message contains any short URLs, this is the first time that a short URL in
              the message was clicked.  This property is undefined for messages that do not contain
              short URLs.
          * Read-only
      
      - service_id (string, max 34 characters)
          * ID of the service that handled the message (for voice calls, the service defines the
              call flow)
          * Read-only
      
      - phone_id (string, max 34 characters)
          * ID of the phone (basic route) that sent or received the message
          * Read-only
      
      - contact_id (string, max 34 characters)
          * ID of the contact that sent or received the message
          * Read-only
      
      - route_id (string, max 34 characters)
          * ID of the custom route that sent the message (if applicable)
          * Read-only
      
      - broadcast_id (string, max 34 characters)
          * ID of the broadcast that this message is part of (if applicable)
          * Read-only
      
      - scheduled_id (string, max 34 characters)
          * ID of the scheduled message that created this message is part of (if applicable)
          * Read-only
      
      - user_id (string, max 34 characters)
          * ID of the Telerivet user who sent the message (if applicable)
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
        (Deprecated) Retrieves a list of MMS parts for this message (only for incoming MMS messages
        received via Telerivet Gateway Android app).
        Note: This only works for MMS messages received via the Telerivet
        Gateway Android app.
        In general, the `media` property of the message is recommended for
        retrieving information about MMS media files.
        
        The return value has the same format as the `mms_parts` property of
        the Message object.
        
        Returns:
            array
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/mms_parts")

    def save(self):
        """
        Saves any fields that have changed for this message.
        """
        super(Message, self).save()

    def resend(self, **options):
        """
        Resends a message, for example if the message failed to send or if it was not delivered. If
        the message was originally in the queued, retrying, failed, or cancelled states, then
        Telerivet will return the same message object. Otherwise, Telerivet will create and return a
        new message object.
        
        Arguments:
            
            - route_id
                * ID of the phone or route to send the message from
          
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/resend", options))

    def cancel(self):
        """
        Cancels sending a message that has not yet been sent. Returns the updated message object.
        Only valid for outgoing messages that are currently in the queued, retrying, or cancelled
        states. For other messages, the API will return an error with the code 'not_cancellable'.
        
        Returns:
            Message
        """
        from .message import Message
        return Message(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/cancel"))

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/messages/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
    
    def _setData(self, data):    
        super(Message, self)._setData(data)
        
        self._label_ids_set = {}
        
        if 'label_ids' in data:
            for label_id in data['label_ids']:            
                self._label_ids_set[label_id] = True
    