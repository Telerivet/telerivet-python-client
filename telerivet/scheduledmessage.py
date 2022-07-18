
from .entity import Entity

class ScheduledMessage(Entity):
    """
    Represents a scheduled message within Telerivet.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the scheduled message
          * Read-only
      
      - content
          * Text content of the scheduled message
          * Read-only
      
      - rrule
          * Recurrence rule for recurring scheduled messages, e.g. 'FREQ=MONTHLY' or
              'FREQ=WEEKLY;INTERVAL=2'; see <https://tools.ietf.org/html/rfc2445#section-4.3.10>
          * Read-only
      
      - timezone_id
          * Timezone ID used to compute times for recurring messages; see
              <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>
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
      
      - recipients_str
          * A string with a human readable description of the first few recipients (possibly
              truncated)
          * Read-only
      
      - group_id
          * ID of the group to send the message to (null if the recipient is an individual
              contact, or if there are multiple recipients)
          * Read-only
      
      - contact_id
          * ID of the contact to send the message to (null if the recipient is a group, or if
              there are multiple recipients)
          * Read-only
      
      - to_number
          * Phone number to send the message to (null if the recipient is a group, or if there
              are multiple recipients)
          * Read-only
      
      - route_id
          * ID of the phone or route the message will be sent from
          * Read-only
      
      - service_id (string, max 34 characters)
          * The service associated with this message (for voice calls, the service defines the
              call flow)
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
      
      - message_type
          * Type of scheduled message
          * Allowed values: sms, mms, ussd, call, service
          * Read-only
      
      - time_created (UNIX timestamp)
          * Time the scheduled message was created in Telerivet
          * Read-only
      
      - start_time (UNIX timestamp)
          * The time that the message will be sent (or first sent for recurring messages)
          * Read-only
      
      - end_time (UNIX timestamp)
          * Time after which a recurring message will stop (not applicable to non-recurring
              scheduled messages)
          * Read-only
      
      - prev_time (UNIX timestamp)
          * The most recent time that Telerivet has sent this scheduled message (null if it has
              never been sent)
          * Read-only
      
      - next_time (UNIX timestamp)
          * The next upcoming time that Telerivet will sent this scheduled message (null if it
              will not be sent again)
          * Read-only
      
      - occurrences (int)
          * Number of times this scheduled message has already been sent
          * Read-only
      
      - is_template (bool)
          * Set to true if Telerivet will render variables like [[contact.name]] in the message
              content, false otherwise
          * Read-only
      
      - track_clicks (boolean)
          * If true, URLs in the message content will automatically be replaced with unique
              short URLs
          * Read-only
      
      - media (array)
          * For text messages containing media files, this is an array of objects with the
              properties `url`, `type` (MIME type), `filename`, and `size` (file size in bytes).
              Unknown properties are null. This property is undefined for messages that do not
              contain media files. Note: For files uploaded via the Telerivet web app, the URL is
              temporary and may not be valid for more than 1 day.
          * Read-only
      
      - route_params (dict)
          * Route-specific parameters to use when sending the message. The parameters object may
              have keys matching the `phone_type` field of a phone (basic route) that may be used to
              send the message. The corresponding value is an object with route-specific parameters
              to use when sending a message with that type of route.
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this scheduled message (copied to Message when sent)
          * Updatable via API
      
      - label_ids (array)
          * IDs of labels to add to the Message
          * Read-only
      
      - project_id
          * ID of the project this scheduled message belongs to
          * Read-only
    """

    def save(self):
        """
        Saves any fields or custom variables that have changed for this scheduled message.
        """
        super(ScheduledMessage, self).save()

    def delete(self):
        """
        Cancels this scheduled message.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/scheduled/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
