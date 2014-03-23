
from .entity import Entity

class ContactServiceState(Entity):
    _has_custom_vars = True

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
