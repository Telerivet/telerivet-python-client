
from .entity import Entity

class ScheduledMessage(Entity):
    def delete(self):
        """
        Cancels this scheduled message.
        
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/scheduled/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
