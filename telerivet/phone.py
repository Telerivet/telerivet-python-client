
from .entity import Entity

class Phone(Entity):
    """
    Represents a basic route (i.e. a phone or gateway) that you use to send/receive messages via
    Telerivet.
    
    Basic Routes were formerly referred to as "Phones" within Telerivet. API
    methods, parameters, and properties related to Basic Routes continue to use the term "Phone"
    to maintain backwards compatibility.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the phone
          * Read-only
      
      - name
          * Name of the phone
          * Updatable via API
      
      - phone_number (string)
          * Phone number or sender ID
          * Updatable via API
      
      - phone_type
          * Type of this phone/route (e.g. android, twilio, nexmo, etc)
          * Read-only
      
      - country
          * 2-letter country code (ISO 3166-1 alpha-2) where phone is from
          * Read-only
      
      - send_paused (bool)
          * True if sending messages is currently paused, false if the phone can currently send
              messages
          * Updatable via API
      
      - time_created (UNIX timestamp)
          * Time the phone was created in Telerivet
          * Read-only
      
      - last_active_time (UNIX timestamp)
          * Approximate time this phone last connected to Telerivet
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this phone. Variable names may be up to 32 characters in
              length and can contain the characters a-z, A-Z, 0-9, and _.
              Values may be strings, numbers, or boolean (true/false).
              String values may be up to 4096 bytes in length when encoded as UTF-8.
              Up to 100 variables are supported per object.
              Setting a variable to null will delete the variable.
          * Updatable via API
      
      - project_id
          * ID of the project this phone belongs to
          * Read-only
      
      - validate_recipient_numbers (bool)
          * Set to true to check that recipient phone numbers appear to be valid before sending
              messages. Messages to invalid phone numbers will fail without being sent. Only applies
              to phones capable of sending messages.
          * Updatable via API
      
      - allowed_recipient_countries (array of strings)
          * Array of 2-letter country codes (ISO 3166-1 alpha-2) to which this phone is allowed
              to send messages. When null, there is no restriction on recipient countries.
          * Updatable via API
      
      - sent_message_limit (int)
          * Maximum number of messages that can be sent from this phone in a given period. When
              the sent_message_count reaches this limit, sending is automatically paused. Set to
              null to disable the limit.
          * Updatable via API
      
      - sent_message_count (int)
          * Number of messages sent from this phone since the counter was last reset (see
              sent_message_epoch). This property is not updated if sent_message_limit is null.
          * Read-only
      
      - sent_message_epoch (UNIX timestamp)
          * The UNIX timestamp when the sent_message_count was last reset to 0.
          * Read-only
      
      - send_delay (number)
          * Number of seconds to wait after sending each message from this phone, to avoid
              exceeding carrier rate limits.
          * Updatable via API
      
      - timezone_id (string)
          * A string specifying the time zone that will be used when implementing quiet hours or
              estimating send times; see [List of tz database time zones Wikipedia
              article](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones). When null, the
              project's default time zone is used.
          * Updatable via API
      
      - quiet_mode (string)
          * Controls behavior during quiet hours (see quiet_start/quiet_end). Possible values
              are 'off' (quiet hours disabled), 'delay' (messages are delayed until quiet hours
              end), or 'confirm' (requires manual confirmation to send during quiet hours).
          * Allowed values: off, delay, confirm
          * Updatable via API
      
      - quiet_start (string)
          * Time of day when quiet hours begin, in HH:MM format (24-hour time) in the phone's
              time zone. Messages sent during quiet hours are delayed or require confirmation
              depending on quiet_mode. Only applicable when quiet_mode is not 'off'.
          * Updatable via API
      
      - quiet_end (string)
          * Time of day when quiet hours end, in HH:MM format (24-hour time) in the phone's time
              zone. Messages sent during quiet hours are delayed or require confirmation depending
              on quiet_mode. Only applicable when quiet_mode is not 'off'.
          * Updatable via API
      
      - battery (int)
          * Current battery level, on a scale from 0 to 100, as of the last time the phone
              connected to Telerivet (only present for Android phones)
          * Read-only
      
      - charging (bool)
          * True if the phone is currently charging, false if it is running on battery, as of
              the last time it connected to Telerivet (only present for Android phones)
          * Read-only
      
      - internet_type
          * String describing the current type of internet connectivity for an Android phone,
              for example WIFI or MOBILE (only present for Android phones)
          * Read-only
      
      - app_version
          * Currently installed version of Telerivet Android app (only present for Android
              phones)
          * Read-only
      
      - android_sdk (int)
          * Android SDK level, indicating the approximate version of the Android OS installed on
              this phone; see [list of Android SDK
              levels](http://developer.android.com/guide/topics/manifest/uses-sdk-element.html#ApiLevels)
              (only present for Android phones)
          * Read-only
      
      - mccmnc
          * Code indicating the Android phone's current country (MCC) and mobile network
              operator (MNC); see [Mobile country code Wikipedia
              article](https://en.wikipedia.org/wiki/Mobile_country_code) (only present for Android
              phones). Note this is a string containing numeric digits, not an integer.
          * Read-only
      
      - manufacturer
          * Android phone manufacturer (only present for Android phones)
          * Read-only
      
      - model
          * Android phone model (only present for Android phones)
          * Read-only
      
      - send_limit (int)
          * Maximum number of SMS messages per hour that can be sent by this Android phone. To
              increase this limit, install additional SMS expansion packs in the Telerivet Gateway
              app. (only present for Android phones)
          * Read-only
      
      - external_account_id (string)
          * Account ID for the external API (e.g. Twilio Account SID, Vonage API Key). Only
              present for routes that support external API configuration. See
              [createPhone](#Project.createPhone) for the meaning of this field for each phone type.
          * Updatable via API
      
      - external_id (string)
          * External phone/resource ID within the external API account (if applicable). Only
              present for routes that support external API configuration.
          * Updatable via API
      
      - external_config (dict)
          * Additional configuration settings specific to the phone_type. Only present for
              routes that support external API configuration. See
              [createPhone](#Project.createPhone) for available settings for each phone type.
          * Updatable via API
      
      - external_setup (dict)
          * Configuration info for routes that require manual webhook setup. Only present for
              routes that require manual configuration of callback URLs with the external provider.
              Contains URL properties for each webhook type that needs to be configured (e.g.,
              `incoming_message_url`, `message_status_url`, `incoming_call_url`).
          * Read-only
      
      - external_secret (string)
          * Secret/API key for the external API (e.g. Twilio Auth Token, Vonage API Secret).
              Only applicable for routes that support external API configuration. Write-only; not
              returned by the API when retrieving a phone.
          * Updatable via API
      
      - url
          * URL to this phone in the Telerivet web app
          * Read-only
    """

    def queryMessages(self, **options):
        """
        Queries messages sent or received by this basic route.
        
        Arguments:
            
            - direction
                * Filter messages by direction
                * Allowed values: incoming, outgoing
            
            - message_type
                * Filter messages by message_type
                * Allowed values: sms, mms, ussd, ussd_session, call, chat, service
            
            - source
                * Filter messages by source
                * Allowed values: phone, provider, web, api, service, webhook, scheduled,
                    integration, mcp
            
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

    def save(self):
        """
        Saves any fields or custom variables that have changed for this basic route.
        """
        super(Phone, self).save()

    def resetSentMessageCount(self):
        """
        Resets this route's sent_message_count to 0 and updates sent_message_epoch to the current
        time. If sending was automatically paused because the previous count reached the limit,
        sending will be resumed.
        """
        self._api.doRequest("POST", self.getBaseApiPath() + "/reset_sent_message_count")

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/phones/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
