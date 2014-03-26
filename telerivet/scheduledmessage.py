
from .entity import Entity

class ScheduledMessage(Entity):
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
