
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
          * Whether to show summary charts (pie charts, bar charts, tables of top values) for
              this data table in the web app
          * Updatable via API
      
      - show_contact_columns (bool)
          * Whether to show 'Contact Name' and 'Phone Number' columns in the web app
          * Updatable via API
      
      - vars (dict)
          * Custom variables stored for this data table. Variable names may be up to 32
              characters in length and can contain the characters a-z, A-Z, 0-9, and _.
              Values may be strings, numbers, or boolean (true/false).
              String values may be up to 4096 bytes in length when encoded as UTF-8.
              Up to 100 variables are supported per object.
              Setting a variable to null will delete the variable.
          * Updatable via API
      
      - project_id
          * ID of the project this data table belongs to
          * Read-only
      
      - url
          * URL to this data table in the Telerivet web app
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
                * Custom variables and values to set for this data row. Variable names may be up to
                    32 characters in length and can contain the characters a-z, A-Z, 0-9, and _.
                    Values may be strings, numbers, or boolean (true/false).
                    String values may be up to 4096 bytes in length when encoded as UTF-8.
                    Up to 100 variables are supported per object.
                    Setting a variable to null will delete the variable.
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/rows", options))

    def importRows(self, **options):
        """
        Creates and/or updates up to 200 rows in a single API call. When creating or updating a
        large number of rows, this method is significantly faster than sending a separate API
        request for each row.
        
        By default, a new row will be created for each item. To update
        existing rows, set the `lookup_key` parameter to match rows by ID, contact, or the value of
        a custom variable.
        
        Arguments:
              * Required
            
            - rows (array)
                * Array of up to 200 objects which may contain the properties `vars` (object),
                    `contact_id` (string), `from_number` (string), and `id` (string). All properties are
                    optional, unless used as a lookup key.
                * Required
            
            - lookup_key
                * The field used to search for a matching row, or 'none' to always create a new row.
                    To search by a custom variable, precede the variable name with 'vars.'.
                * Allowed values: none, id, contact_id, vars.variable_name
                * Default: none
          
        Returns:
            (associative array)
              - rows (array)
                  * List of objects representing each row, in the same order as provided in the
                      `rows` parameter in the API request.
        """
        data = self._api.doRequest("POST", self.getBaseApiPath() + "/import_rows", options)
        return data

    def getRowById(self, row_id):
        """
        Retrieves the row in the given table with the given ID.
        
        Arguments:
          - row_id
              * ID of the row
              * Required
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/rows/%s" % (row_id)))

    def initRowById(self, row_id):
        """
        Initializes the row in the given table with the given ID, without making an API request.
        
        Arguments:
          - row_id
              * ID of the row
              * Required
          
        Returns:
            DataRow
        """
        from .datarow import DataRow
        return DataRow(self._api, {'project_id': self.project_id, 'table_id': self.id, 'row_id': row_id}, False)

    def queryViews(self, **options):
        """
        Queries views of this data table.
        
        Arguments:
            
            - name
                * Filter views by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
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
            APICursor (of DataView)
        """
        from .dataview import DataView
        return self._api.newApiCursor(DataView, self.getBaseApiPath() + "/views", options)

    def createView(self, **options):
        """
        Creates a new view of this data table, defined by a filter on its rows. The view's filter
        conditions cannot be changed after the view is created (although the view can be renamed or
        deleted).
        
        Telerivet will automatically store the count of rows matching each
        data view once a day, making it possible to retrieve historical statistics for the number of
        rows matching the filter, but only for dates after the view is created.
        
        Arguments:
              * Required
            
            - name (string, max 64 characters)
                * Name of the view (must be unique within the data table)
                * Required
            
            - filters (dict)
                * Key-value pairs of conditions that rows must match to be included in the view. To
                    filter by a custom variable, precede the variable name with 'vars.' (conditions on
                    custom variables may also be provided as a nested object under a `vars` key, e.g.
                    `{"vars": {"q1": "yes"}}`); other supported keys are `id`, `time_created`,
                    `time_updated`, `contact_id`, `contact_name`, and `from_number`. Each value is
                    either a value to match exactly, or an object with an operator such as `ne`,
                    `prefix`, `gte`, `gt`, `lte`, `lt`, `exists`, or `not_exists` as the key (e.g.
                    `{"gte": 10}`).
                * Required
          
        Returns:
            DataView
        """
        from .dataview import DataView
        return DataView(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/views", options))

    def getViewById(self, view_id):
        """
        Retrieves the view of the given table with the given ID.
        
        Arguments:
          - view_id
              * ID of the view
              * Required
          
        Returns:
            DataView
        """
        from .dataview import DataView
        return DataView(self._api, self._api.doRequest("GET", self.getBaseApiPath() + "/views/%s" % (view_id)))

    def initViewById(self, view_id):
        """
        Initializes the view of the given table with the given ID, without making an API request.
        
        Arguments:
          - view_id
              * ID of the view
              * Required
          
        Returns:
            DataView
        """
        from .dataview import DataView
        return DataView(self._api, {'project_id': self.project_id, 'table_id': self.id, 'view_id': view_id}, False)

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
        
        The variable path parameter can contain the characters a-z, A-Z,
        0-9, and _, and may be up to 32 characters in length.
        
        Arguments:
          - variable
              * The variable name of the field to create or update.
              * Required
          
              * Required
            
            - name (string, max 64 characters)
                * Display name for the field
            
            - type (string)
                * Field type
                * Allowed values: text, long_text, secret, phone_number, email, url, audio, date,
                    date_time, number, boolean, checkbox, select, radio, route
            
            - order (int)
                * Order in which to display the field
            
            - items (array)
                * Array of up to 100 objects containing `value` and `label` string properties to
                    show when type is `select` or `radio`. Each `value` and `label` must be between 1
                    and 256 characters in length.
                * Required if type is `select` or `radio`
            
            - readonly (bool)
                * Set to true to prevent editing the field in the Telerivet web app
            
            - lookup_key (bool)
                * Set to true to allow using this field as a lookup key when importing rows via the
                    Telerivet web app
          
        Returns:
            object
        """
        return self._api.doRequest("POST", self.getBaseApiPath() + "/fields/%s" % (variable), options)

    def updateFields(self, **options):
        """
        Updates metadata for one or more fields (columns) in the data table. Only the specified
        fields are updated; other fields are not affected.
        
        To delete a field, include an object with the `variable` and
        `delete` properties set (e.g. `{"variable": "my_field", "delete": true}`). Deleting a field
        will also clear the corresponding variable on all rows in the table.
        
        Arguments:
              * Required
            
            - metadata (array)
                * Array of up to 100 objects describing the fields to create, update, or delete.
                    Each object must contain a `variable` property. Only the properties provided for
                    each field will be updated.
                * Required
          
        Returns:
            array
        """
        return self._api.doRequest("POST", self.getBaseApiPath() + "/fields", options)

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
