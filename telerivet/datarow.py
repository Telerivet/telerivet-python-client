
from .entity import Entity

class DataRow(Entity):
    def save(self):
        """
        Saves any fields or custom variables that have changed for this data row.
        
        """
        super(DataRow, self).save()

    def delete(self):
        """
        Deletes this data row.
        
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/tables/%(table_id)s/rows/%(id)s" % {'project_id': self.project_id, 'table_id': self.table_id, 'id': self.id} 
