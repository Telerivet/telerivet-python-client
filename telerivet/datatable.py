
from .entity import Entity

class DataTable(Entity):
    """
    Represents a custom data table that can store arbitrary rows.
    
    For example, poll services use data tables to store a row for each response.
    
    DataTables are schemaless -- each row simply stores custom variables. Each
    variable name is equivalent to a different "column" of the data table.
    Telerivet refers to these variables/columns as "fields", and automatically
    creates a new field for each variable name used in a row of the table.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the data table
          * Read-only
      
      - name
          * Name of the data table
          * Updatable via API
      
      - num_rows (int)
          * Number of rows in the table. For performance reasons, this number may sometimes be
              out-of-date.
          * Read-only
      
      - show_add_row (bool)
          * Whether to allow adding or importing rows via the web app
          * Updatable via API
      
      - show_stats (bool)
          * Whether to show row statistics in the web app
          * Updatable via API
      
      - show_contact_columns (bool)
          * Whether to show 'Contact Name' and 'Phone Number' columns in the web app
          * Updatable via API
      
      - vars (dict)
          * Custom variables stored for this data table
          * Updatable via API
      
      - project_id
          * ID of the project this data table belongs to
          * Read-only
    """

    def queryRows(self, **options):
        """
        Queries rows in this data table.
        
        Arguments:
            
            - time_created (UNIX timestamp)
                * Filter data rows by the time they were created
                * Allowed modifiers: time_created[min], time_created[max]
            
            - contact_id
                * Filter data rows associated with a particular contact
            
            - vars (dict)
                * Filter data rows by value of a custom variable (e.g. vars[q1], vars[foo], etc.)
                * Allowed modifiers: vars[foo][ne], vars[foo][prefix], vars[foo][not_prefix],
                    vars[foo][gte], vars[foo][gt], vars[foo][lt], vars[foo][lte], vars[foo][min],
                    vars[foo][max], vars[foo][exists]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
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
        Retrieves the row in the given table with the given ID.
        
        Arguments:
          - id
              * ID of the row
              * Required
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/rows/%s" % (id)))

    def initRowById(self, id):
        """
        Initializes the row in the given table with the given ID, without making an API request.
        
        Arguments:
          - id
              * ID of the row
              * Required
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, {'project_id': self.project_id, 'table_id': self.id, 'id': id}, False)

    def getFields(self):
        """
        Gets a list of all fields (columns) defined for this data table. The return value is an
        array of objects with the properties 'name', 'variable', 'type', 'order', 'readonly', and
        'lookup_key'. (Fields are automatically created any time a DataRow's 'vars' property is
        updated.)
        
        Returns:
            array
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/fields")

    def setFieldMetadata(self, variable, **options):
        """
        Allows customizing how a field (column) is displayed in the Telerivet web app.
        
        Arguments:
          - variable
              * The variable name of the field to create or update.
              * Required
          
              * Required
            
            - name (string, max 64 characters)
                * Display name for the field
            
            - type (string)
                * Field type
                * Allowed values: text, long_text, phone_number, email, url, audio, date, date_time,
                    number, boolean, select
            
            - order (int)
                * Order in which to display the field
            
            - items (array)
                * Array of up to 100 objects containing `value` and `label` string properties to
                    show in the dropdown list when type is `select`. Each `value` and `label` must be
                    between 1 and 256 characters in length.
                * Required if type is `select`
            
            - readonly (bool)
                * Set to true to prevent editing the field in the Telerivet web app
            
            - lookup_key (bool)
                * Set to true to allow using this field as a lookup key when importing rows via the
                    Telerivet web app
          
        Returns:
            object
        """
        return self._api.doRequest("POST", self.getBaseApiPath() + "/fields/%s" % (variable), options)

    def countRowsByValue(self, variable):
        """
        Returns the number of rows for each value of a given variable. This can be used to get the
        total number of responses for each choice in a poll, without making a separate query for
        each response choice. The return value is an object mapping values to row counts, e.g.
        `{"yes":7,"no":3}`
        
        Arguments:
          - variable
              * Variable of field to count by.
              * Required
          
        Returns:
            object
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/count_rows_by_value", {'variable': variable})

    def save(self):
        """
        Saves any fields that have changed for this data table.
        """
        super(DataTable, self).save()

    def delete(self):
        """
        Permanently deletes the given data table, including all its rows
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/tables/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
