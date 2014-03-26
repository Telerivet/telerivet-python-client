
from .entity import Entity

class MobileMoneyReceipt(Entity):
    def save(self):
        """
        Saves any fields or custom variables that have changed for this mobile money receipt.
        
        """
        super(MobileMoneyReceipt, self).save()

    def delete(self):
        """
        Deletes this receipt.
        
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/receipts/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
