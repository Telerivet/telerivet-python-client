
from .entity import Entity

class MobileMoneyReceipt(Entity):
    def delete(self):
        """
        Deletes this receipt.
        
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/receipts/%(receipt_id)s" % {'project_id': self.project_id, 'receipt_id': self.receipt_id} 
