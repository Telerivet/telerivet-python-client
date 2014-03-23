
from .entity import Entity

class DataTable(Entity):
    def queryRows(self, **options):
        """
        Queries rows in this data table.
        
        Arguments:
            
            - time_created (UNIX timestamp)
                * Filter data rows by the time they were created
                * Allowed modifiers: time_created[ne], time_created[min], time_created[max]
            
            - vars (dict)
                * Filter data rows by value of a custom variable (e.g. vars[q1], vars[foo], etc.)
                * Allowed modifiers: vars[foo][exists], vars[foo][ne], vars[foo][prefix],
                    vars[foo][not_prefix], vars[foo][gte], vars[foo][gt], vars[foo][lt], vars[foo][lte],
                    vars[foo][min], vars[foo][max]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 200)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of DataRow)
        """
        from .datarow import DataRow
        return self._api.newApiCursor(DataRow, self.getBaseApiPath() + "/rows", options)

    def createRow(self, **options):
        """
        Adds a new row to this data table.
        
        Arguments:
            
            - contact_id
                * ID of the contact that this row is associated with (if applicable)
            
            - from_number (string)
                * Phone number that this row is associated with (if applicable)
            
            - vars
                * Custom variables and values to set for this data row
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/rows", options))

    def getRowById(self, id):
        """
        Gets a row in this table by its ID.
        
        Note: This does not make any API requests until you access a property of the DataRow.
        
        Arguments:
          - id (ID of the row)
              * Required
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, {'project_id': self.project_id, 'table_id': self.id, 'id': id}, False)

    def save(self):
        """
        Saves any fields that have changed for this data table.
        
        """
        super(DataTable, self).save()

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/tables/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
