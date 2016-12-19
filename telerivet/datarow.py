
from .entity import Entity

class DataRow(Entity):
    """
    Represents a row in a custom data table.
    
    For example, each response to a poll is stored as one row in a data table.
    If a poll has a question with ID 'q1', the verbatim response to that question would be
    stored in row.vars.q1, and the response code would be stored in row.vars.q1_code.
    
    Each custom variable name within a data row corresponds to a different
    column/field of the data table.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the data row
          * Read-only
      
      - contact_id
          * ID of the contact this row is associated with (or null if not associated with any
              contact)
          * Updatable via API
      
      - from_number (string)
          * Phone number that this row is associated with (or null if not associated with any
              phone number)
          * Updatable via API
      
      - vars (dict)
          * Custom variables stored for this data row
          * Updatable via API
      
      - time_created (UNIX timestamp)
          * The time this row was created in Telerivet
          * Read-only
      
      - time_updated (UNIX timestamp)
          * The time this row was last updated in Telerivet
          * Read-only
      
      - table_id
          * ID of the table this data row belongs to
          * Read-only
      
      - project_id
          * ID of the project this data row belongs to
          * Read-only
    """

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
