
from .entity import Entity

class Campaign(Entity):
    """
    A campaign is something that is sent to a group of contacts on a particular schedule.
    
    Depending on the campaign type, a campaign may send a text message, make a
    voice call, or trigger an automated service. A campaign may either send a single broadcast
    at once, or send multiple broadcasts to different contacts over time.
    
    Campaigns are initially created as a draft and can be edited and previewed
    before being sent. This supports a workflow where campaigns can be drafted via the API, and
    subsequently edited, approved, and sent via either the web app or the API. Once sent, a
    campaign creates one or more broadcasts to deliver messages to the target recipients.
    
    Campaigns build on top of other core entity types including broadcasts and
    scheduled messages. Although it is possible to send broadcasts or schedule messages directly
    via the API, campaigns can be used in order to provide the ability to save drafts, allow
    manual editing and approval before sending, or to organize broadcasts within Telerivet.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the campaign
          * Read-only
      
      - name
          * Name of the campaign, which must be unique within the project. The campaign name is
              only visible within Telerivet, and does not appear in the messages sent to contacts.
          * Updatable via API
      
      - campaign_type
          * Type of the campaign. The following campaign types are available:
              
              - `broadcast_text` - Send a text message to a group of contacts
              - `broadcast_call` - Send a voice call to a group of contacts
              - `broadcast_svc` - Trigger a service for a group of contacts
              - `relative` - Send a series of messages over time relative to
              when each contact was added to a group
              - `anniversary` - Send messages on recurring dates (e.g.
              birthdays, anniversaries)
          * Allowed values: broadcast_text, broadcast_call, broadcast_svc, relative, anniversary
          * Read-only
      
      - status
          * Current status of the campaign
          * Allowed values: draft, scheduled, sent, pending_review
          * Read-only
      
      - group_id
          * ID of the group of contacts that the campaign will be sent to
          * Updatable via API
      
      - exclude_group_id
          * ID of a group of contacts to exclude from the campaign
          * Updatable via API
      
      - route_id
          * ID of the phone or route used to send the campaign
          * Updatable via API
      
      - broadcast_id
          * ID of the most recent broadcast created by this campaign, if applicable
          * Read-only
      
      - estimated_count (int)
          * Estimated number of messages that will be sent in this campaign
          * Read-only
      
      - message_count (int)
          * Number of messages that have been sent in this campaign
          * Read-only
      
      - respondent_group_id
          * ID of a group to add contacts to after they respond to the campaign
          * Updatable via API
      
      - clicked_group_id
          * ID of a group to add contacts to after they click a link in the campaign
          * Updatable via API
      
      - label_ids (array)
          * List of IDs of labels applied to messages sent by this campaign
          * Updatable via API
      
      - schedule_mode
          * Indicates whether the campaign should be sent immediately or at a future time
              (applies to broadcast campaign types). If `schedule_time` is set, `schedule_mode` is
              automatically set to `at_time`. If `schedule_mode` is set to `immediate` or `null`,
              `schedule_time` is automatically cleared.
              
              Note that after setting schedule_mode to "immediate" on a campaign
              with the `draft` status, the campaign will not actually be sent until the API method
              is called to [send the campaign](#Campaign.send).
          * Allowed values: immediate, at_time
          * Updatable via API
      
      - schedule_time (UNIX timestamp)
          * The time to send the campaign, as a UNIX timestamp (applies to broadcast campaign
              types). Setting this to a non-null value automatically sets `schedule_mode` to
              `at_time`.
              
              Note that after setting schedule_time on a campaign with the
              `draft` status, the campaign will not actually be scheduled until the API method is
              called to [schedule the campaign](#Campaign.send).
          * Updatable via API
      
      - content (string)
          * Text content of the message (applies to `broadcast_text` campaigns), or the
              text-to-speech text for voice calls (applies to `broadcast_call` campaigns). May
              contain variables like `[[contact.name]]`.
              
              [(See available variables)](#variables)
          * Updatable via API
      
      - media (array)
          * Array of media attachments (applies to `broadcast_text` campaigns).
          * Read-only
      
      - route_params (dict)
          * Route-specific parameters for the message (applies to `broadcast_text` campaigns).
              See [Route-Specific Parameters](#route_params).
          * Updatable via API
      
      - track_clicks (boolean)
          * Whether to shorten links and track link clicks (applies to `broadcast_text`
              campaigns).
          * Updatable via API
      
      - short_link_params (dict)
          * Parameters for short links when `track_clicks` is enabled (applies to
              `broadcast_text` campaigns).
          * Updatable via API
      
      - audio_url
          * For voice calls, the URL of an MP3 file to play when the contact answers the call
              (applies to `broadcast_call` campaigns)
          * Updatable via API
      
      - tts_lang
          * For voice calls, the language of the text-to-speech voice (applies to
              `broadcast_call` campaigns)
          * Allowed values: en-US, en-GB, en-GB-WLS, en-AU, en-IN, da-DK, nl-NL, fr-FR, fr-CA,
              de-DE, is-IS, it-IT, pl-PL, pt-BR, pt-PT, ru-RU, es-ES, es-US, sv-SE
          * Updatable via API
      
      - tts_voice
          * For voice calls, the text-to-speech voice (applies to `broadcast_call` campaigns)
          * Allowed values: female, male
          * Updatable via API
      
      - service_id
          * ID of the service associated with this campaign (applies to `broadcast_call` or
              `broadcast_svc` campaigns)
          * Read-only
      
      - date_variable
          * Custom contact variable storing date or date/time values relative to which messages
              will be scheduled (applies to `relative` and `anniversary` campaigns)
          * Updatable via API
      
      - items (array)
          * Array of campaign items (applies to `relative` and `anniversary` campaigns). Each
              item defines a scheduled message with timing and content.
          * Updatable via API
      
      - message_type
          * Type of messages sent by this campaign, or null if not applicable
          * Read-only
      
      - timezone_id
          * The ID of the timezone used for scheduling messages in this campaign, or null to use
              the project's default timezone
          * Updatable via API
      
      - time_created (UNIX timestamp)
          * Time the campaign was created in Telerivet
          * Read-only
      
      - time_updated (UNIX timestamp)
          * Time the campaign was last updated in Telerivet
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this campaign. Variable names may be up to 32 characters
              in length and can contain the characters a-z, A-Z, 0-9, and _.
              Values may be strings, numbers, or boolean (true/false).
              String values may be up to 4096 bytes in length when encoded as UTF-8.
              Up to 100 variables are supported per object.
              Setting a variable to null will delete the variable.
          * Updatable via API
      
      - url
          * URL to view the campaign in the Telerivet web app
          * Read-only
      
      - url_edit
          * URL to edit the campaign in the Telerivet web app
          * Read-only
      
      - url_send
          * URL to preview and send the campaign in the Telerivet web app
          * Read-only
      
      - user_id
          * ID of the Telerivet user who created the campaign
          * Read-only
      
      - project_id
          * ID of the project this campaign belongs to
          * Read-only
    """

    def save(self):
        """
        Saves any fields or custom variables that have changed for this campaign.
        """
        super(Campaign, self).save()

    def send(self):
        """
        Sends or schedules this campaign. The campaign must be in the `draft` or `scheduled` status,
        and must be fully configured (e.g. with a group, route, and message content).
        
        For broadcast campaigns, this will send the campaign immediately if
        the campaign's `schedule_mode` is `immediate`. If `schedule_mode` is `at_time`, it will
        schedule the campaign to be sent at the time of the `schedule_time` timestamp.
        
        For relative and anniversary campaigns, this will schedule the
        campaign according to the configuration in the `items` and `date_variable` properties.
        
        Returns:
            Campaign
        """
        from .campaign import Campaign
        return Campaign(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/send"))

    def unschedule(self):
        """
        Cancels a scheduled campaign, reverting it to the `draft` status. The campaign must be in
        the `scheduled` or `pending_review` status.
        
        Returns:
            Campaign
        """
        from .campaign import Campaign
        return Campaign(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/unschedule"))

    def delete(self):
        """
        Deletes this campaign. Any scheduled messages will be cancelled.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/campaigns/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
