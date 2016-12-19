
from .entity import Entity

class ContactServiceState(Entity):
    """
    Represents the current state of a particular contact for a particular Telerivet service.
    
    Some automated services (including polls) are 'stateful'. For polls,
    Telerivet needs to keep track of which question the contact is currently answering, and
    stores store the ID of each contact's current question (e.g. 'q1' or 'q2') as the ID of the
    contact's state for the poll service. Any type of conversation-like service will also need
    to store state for each contact.
    
    For this type of entity, the 'id' field is NOT a read-only unique ID (unlike
    all other types of entities). Instead it is an arbitrary string that identifies the
    contact's current state within your poll/conversation; many contacts may have the same state
    ID, and it may change over time. Additional custom fields may be stored in the 'vars'.
    
    Initially, the state 'id' for any contact is null. When saving the state,
    setting the 'id' to null is equivalent to resetting the state (so all 'vars' will be
    deleted); if you want to save custom variables, the state 'id' must be non-null.
    
    Many Telerivet services are stateless, such as auto-replies or keyword-based
    services where the behavior only depends on the current message, and not any previous
    messages sent by the same contact. Telerivet doesn't store any state for contacts that
    interact with stateless services.
    
    Fields:
    
      - id (string, max 63 characters)
          * Arbitrary string representing the contact's current state for this service, e.g.
              'q1', 'q2', etc.
          * Updatable via API
      
      - contact_id
          * ID of the contact
          * Read-only
      
      - service_id
          * ID of the service
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this contact/service state
          * Updatable via API
      
      - time_created (UNIX timestamp)
          * Time the state was first created in Telerivet
          * Read-only
      
      - time_updated (UNIX timestamp)
          * Time the state was last updated in Telerivet
          * Read-only
      
      - project_id
          * ID of the project this contact/service state belongs to
          * Read-only
    """

    def save(self):
        """
        Saves the state id and any custom variables for this contact. If the state id is null, this
        is equivalent to calling reset().
        """
        super(ContactServiceState, self).save()

    def reset(self):
        """
        Resets the state for this contact for this service.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/services/%(service_id)s/states/%(contact_id)s" % {'project_id': self.project_id, 'service_id': self.service_id, 'contact_id': self.contact_id} 
