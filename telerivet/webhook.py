
from .entity import Entity

class Webhook(Entity):
    """
    Represents a webhook that is triggered when specific events occur within a project.
    
    Webhooks allow your server to receive HTTP POST requests when certain events
    happen, such as when a message's status changes or when a contact is updated.
    
    When an event occurs that matches a webhook's event types, Telerivet will
    send an HTTP POST request to the webhook URL with information about the event. For more
    information about the webhook request format, see the [Webhook API](/api/webhook)
    documentation.
    
    Note: The Webhook object is not used for notifying your server when incoming
    messages are received. To notify a URL when incoming messages are received, you can
    configure a webhook by [creating a Service](#Project.createService) with type
    incoming_message_webhook.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the webhook
          * Read-only
      
      - url
          * URL that webhook requests are sent to
          * Updatable via API
      
      - secret
          * Secret included with webhook requests for authentication (sent as HTTP basic auth
              password with username 'telerivet')
          * Updatable via API
      
      - events (array of strings)
          * Array of event types that trigger this webhook. Possible values: `send_status`
              (message status updates), `send_broadcast` (broadcast sent), `contact_update` (contact
              added/updated/deleted), `message_metadata` (message metadata updated)
          * Updatable via API
      
      - project_id
          * ID of the project this webhook belongs to
          * Read-only
    """

    def save(self):
        """
        Saves any fields that have changed for this webhook.
        """
        super(Webhook, self).save()

    def delete(self):
        """
        Deletes the webhook.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/webhooks/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
