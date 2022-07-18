
class API:
    """
    
    """

    client_version = '1.6.1'

    """
        Initializes a client handle to the Telerivet REST API.
        
        Each API key is associated with a Telerivet user account, and all
        API actions are performed with that user's permissions. If you want to restrict the
        permissions of an API client, simply add another user account at
        <https://telerivet.com/dashboard/users> with the desired permissions.
        
        Arguments:
          - api_key (Your Telerivet API key; see <https://telerivet.com/dashboard/api>)
              * Required
    """
    def __init__(self, api_key, api_url = 'https://api.telerivet.com/v1'):
        self.api_key = api_key
        self.api_url = api_url
        self.num_requests = 0
        self.session = None

    def getProjectById(self, id):
        """
        Retrieves the Telerivet project with the given ID.
        
        Arguments:
          - id
              * ID of the project -- see <https://telerivet.com/dashboard/api>
              * Required
          
        Returns:
            Project
        """
        from .project import Project
        return Project(self, self.doRequest("GET", self.getBaseApiPath() + "/projects/%s" % (id)))

    def initProjectById(self, id):
        """
        Initializes the Telerivet project with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the project -- see <https://telerivet.com/dashboard/api>
              * Required
          
        Returns:
            Project
        """
        from .project import Project
        return Project(self, {'id': id}, False)

    def queryProjects(self, **options):
        """
        Queries projects accessible to the current user account.
        
        Arguments:
            
            - name
                * Filter projects by name
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
            APICursor (of Project)
        """
        from .project import Project
        return self.newApiCursor(Project, self.getBaseApiPath() + "/projects", options)

    def getOrganizationById(self, id):
        """
        Retrieves the Telerivet organization with the given ID.
        
        Arguments:
          - id
              * ID of the organization -- see <https://telerivet.com/dashboard/api>
              * Required
          
        Returns:
            Organization
        """
        from .organization import Organization
        return Organization(self, self.doRequest("GET", self.getBaseApiPath() + "/organizations/%s" % (id)))

    def initOrganizationById(self, id):
        """
        Initializes the Telerivet organization with the given ID without making an API request.
        
        Arguments:
          - id
              * ID of the organization -- see <https://telerivet.com/dashboard/api>
              * Required
          
        Returns:
            Organization
        """
        from .organization import Organization
        return Organization(self, {'id': id}, False)

    def queryOrganizations(self, **options):
        """
        Queries organizations accessible to the current user account.
        
        Arguments:
            
            - name
                * Filter organizations by name
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
            APICursor (of Organization)
        """
        from .organization import Organization
        return self.newApiCursor(Organization, self.getBaseApiPath() + "/organizations", options)

    def getBaseApiPath(self):
        return "" 
    def encodeParamsRec(self, paramName, value, res):
        if value is None:
            return

        if isinstance(value,(list, tuple)):
            for i, val in enumerate(value):
                self.encodeParamsRec(paramName + "[" +i + "]", val, res)
        elif isinstance(value,dict):
            for key, val in value.items():
                self.encodeParamsRec(paramName + "[" + key + "]", val, res)
        elif isinstance(value,bool):
            res[paramName] = 1 if value else 0
        else:
            res[paramName] = value

    def getUrlParams(self, params):
        res = {}
        if params is not None:
            for key, value in params.items():
                self.encodeParamsRec(key, value, res)
        return res

    def doRequest(self, method, path, params = None):
        import requests, os, json, sys, zlib

        url = self.api_url + path

        if self.session is None:
            self.session = requests.Session()

        version_info = sys.version_info

        headers = {
            "User-Agent": "Telerivet Python Client/%s Python/%s.%s.%s OS/%s" % (API.client_version, version_info[0], version_info[1], version_info[2], sys.platform)
        }
        data = None
        query = None
        if method == 'POST' or method == 'PUT':
            headers['Content-Type'] = "application/json"
            data = json.dumps(params)

            if len(data) >= 400:
                headers['Content-Encoding'] = 'gzip'
                data_bytes = bytes(data, 'UTF-8') if version_info[0] >= 3 else data
                gzip_compress = zlib.compressobj(-1, zlib.DEFLATED, zlib.MAX_WBITS | 16) # add gzip header
                gzip_data = gzip_compress.compress(data_bytes) + gzip_compress.flush()
                data = gzip_data
        else:
            query = self.getUrlParams(params)

        self.num_requests += 1

        response = self.session.request(method, url,
            headers = headers,
            data = data,
            params = query,
            auth = (self.api_key, ''),
            timeout = 60,
            verify = True
        )

        try:
            res = response.json()
        except ValueError as e:
            raise IOError("Unexpected response from Telerivet API (HTTP {}): {}".format(response.status_code, response.content))

        if "error" in res:
            error = res['error']
            error_code = error['code']

            if error_code == 'invalid_param':
                raise InvalidParameterException(error['message'], error['code'], error['param'])
            elif error_code == 'not_found':
                raise NotFoundException(error['message'], error['code']);
            else:
                raise APIException(error['message'], error['code'])
        else:
            return res

    def newApiCursor(self, item_cls, path, options):
        from .apicursor import APICursor
        return APICursor(self, item_cls, path, options)

class TelerivetException(Exception):
    pass

class APIException(TelerivetException):

    def __init__(self, message, code):
        super(APIException, self).__init__(message)
        self.code = code

class NotFoundException(APIException):
    pass

class InvalidParameterException(APIException):
    def __init__(self, message, code, param):
        super(InvalidParameterException, self).__init__(message, code)
        self.param = param
