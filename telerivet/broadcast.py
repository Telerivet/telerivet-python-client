
from .entity import Entity

class Broadcast(Entity):
    """
    Represents a collection of related outgoing messages.
    Typically, messages in a broadcast have the same content template and were
    sent at the same time; however, a broadcast can also contain messages with unrelated content
    and messages that were sent at different times.
    A broadcast is automatically created when sending a message to a group of
    contacts.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the broadcast
          * Read-only
      
      - recipients (array of objects)
          * List of recipients. Each recipient is an object with a string `type` property, which
              may be `"phone_number"`, `"group"`, or `"filter"`.
              
              If the type is `"phone_number"`, the `phone_number` property will
              be set to the recipient's phone number.
              
              If the type is `"group"`, the `group_id` property will be set to
              the ID of the group, and the `group_name` property will be set to the name of the
              group.
              
              If the type is `"filter"`, the `filter_type` property (string) and
              `filter_params` property (object) describe the filter used to send the broadcast. (API
              clients should not rely on a particular value or format of the `filter_type` or
              `filter_params` properties, as they may change without notice.)
          * Read-only
      
      - title
          * Title of the broadcast. If a title was not provided when the broadcast was sent, it
              is automatically set to a human readable description of the first few recipients
              (possibly truncated)
          * Read-only
      
      - time_created (UNIX timestamp)
          * Time the broadcast was sent in Telerivet
          * Read-only
      
      - last_message_time (UNIX timestamp)
          * Time the most recent message was queued to send in this broadcast
          * Read-only
      
      - last_send_time (UNIX timestamp)
          * Time the most recent message was sent (or failed to send) in this broadcast, or null
              if no messages have been sent yet
          * Read-only
      
      - status_counts (dict)
          * An object whose keys are the possible status codes (`"queued"`, `"sent"`,
              `"failed"`, `"failed_queued"`, `"delivered"`, `"not_delivered"`, and `"cancelled"`),
              and whose values are the number of messages in the broadcast currently in that status.
          * Read-only
      
      - message_count (int)
          * The total number of messages created for this broadcast. For large broadcasts, the
              messages may not be created immediately after the broadcast is sent. The
              `message_count` includes messages in any status, including messages that are still
              queued.
          * Read-only
      
      - estimated_count (int)
          * The estimated number of messages in this broadcast when it is complete. The
              `estimated_count` is calculated at the time the broadcast is sent. When the broadcast
              is completed, the `estimated_count` may differ from `message_count` if there are any
              blocked contacts among the recipients (blocked contacts are included in
              `estimated_count` but not in `message_count`), if any contacts don't have phone
              numbers, or if the group membership changed while the broadcast was being sent.
          * Read-only
      
      - message_type
          * Type of message sent from this broadcast
          * Allowed values: sms, mms, ussd, call, service
          * Read-only
      
      - content (string)
          * The text content of the message (null for USSD messages and calls)
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
      
      - is_template (bool)
          * Set to true if Telerivet will render variables like [[contact.name]] in the message
              content, false otherwise
          * Read-only
      
      - status
          * The current status of the broadcast.
          * Allowed values: queuing, sending, complete, cancelled
          * Read-only
      
      - source
          * How the message originated within Telerivet
          * Allowed values: phone, provider, web, api, service, webhook, scheduled, integration
          * Read-only
      
      - simulated (bool)
          * Whether this message was simulated within Telerivet for testing (and not actually
              sent to or received by a real phone)
          * Read-only
      
      - track_clicks (boolean)
          * If true, URLs in the message content will automatically be replaced with unique
              short URLs.
          * Read-only
      
      - clicked_count (int)
          * The number of messages in this broadcast containing short links that were clicked.
              At most one click per message is counted. If track_clicks is false, this property will
              be null.
          * Read-only
      
      - label_ids (array)
          * List of IDs of labels applied to all messages in the broadcast
          * Read-only
      
      - media (array)
          * For text messages containing media files, this is an array of objects with the
              properties `url`, `type` (MIME type), `filename`, and `size` (file size in bytes).
              Unknown properties are null. This property is undefined for messages that do not
              contain media files. Note: For files uploaded via the Telerivet web app, the URL is
              temporary and may not be valid for more than 1 day.
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this broadcast
          * Read-only
      
      - route_params (dict)
          * Route-specific parameters for the messages in the broadcast. The parameters object
              may have keys matching the `phone_type` field of a phone (basic route) that may be
              used to send messages in this broadcast. The corresponding value is an object with
              route-specific parameters to use when sending messages with that type of route.
          * Read-only
      
      - price (number)
          * The total price of all messages in this broadcast, if known.
          * Read-only
      
      - price_currency
          * The currency of the message price, if applicable.
          * Read-only
      
      - reply_count (int)
          * The number of replies received in response to a message sent in this broadcast.
              (Replies are not included in `message_count` ,`status_counts`, or `price`.)
          * Read-only
      
      - last_reply_time (UNIX timestamp)
          * Time the most recent reply was received in response to a message sent in this
              broadcast, or null if no replies have been sent yet
          * Read-only
      
      - route_id (string, max 34 characters)
          * ID of the phone or route used to send the broadcast (if applicable)
          * Read-only
      
      - service_id (string, max 34 characters)
          * The service associated with this broadcast (for voice calls, the service defines the
              call flow)
          * Read-only
      
      - user_id (string, max 34 characters)
          * ID of the Telerivet user who sent the broadcast (if applicable)
          * Read-only
      
      - project_id
          * ID of the project this broadcast belongs to
          * Read-only
    """

    def cancel(self):
        """
        Cancels sending a broadcast that has not yet been completely sent. No additional messages
        will be queued, and any existing queued messages will be cancelled when they would otherwise
        have been sent (except for messages already queued on the Telerivet Android app, which will
        not be automatically cancelled).
        
        Returns:
            Broadcast
        """
        from .broadcast import Broadcast
        return Broadcast(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/cancel"))

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/broadcasts/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
