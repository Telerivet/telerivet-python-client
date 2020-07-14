class APICursor:
    """
    An easy-to-use interface for interacting with API methods that return collections of objects
    that may be split into multiple pages of results.
    
    Using the APICursor, you can easily iterate over query results without
    having to manually fetch each page of results.
    """

    def __init__(self, api, item_cls, path, params = None):
        if params is None:
            params = {}

        if 'count' in params:
            raise TelerivetException("Cannot construct APICursor with 'count' parameter. Call the count() method instead.")

        self.api = api
        self.item_cls = item_cls
        self.path = path
        self.params = params

        self._count = -1
        self.pos = None
        self.data = None
        self.truncated = None
        self.next_marker = None
        self._limit = None
        self.offset = 0

    def limit(self, limit):
        """
        Limits the maximum number of entities fetched by this query.
        
        By default, iterating over the cursor will automatically fetch
        additional result pages as necessary. To prevent fetching more objects than you need, call
        this method to set the maximum number of objects retrieved from the API.
        
        Arguments:
          - limit (int)
              * The maximum number of entities to fetch from the server (may require multiple API
                  calls if greater than 200)
              * Required
          
        Returns:
            the current APICursor object
        """

        self._limit = limit
        return self

    def count(self):
        """
        Returns the total count of entities matching the current query, without actually fetching
        the entities themselves.
        
        This is much more efficient than all() if you only need the count,
        as it only results in one API call, regardless of the number of entities matched by the
        query.
        
        Returns:
            int
        """

        if self._count == -1:
            params = self.params.copy()
            params['count'] = 1

            res = self.api.doRequest("GET", self.path, params)
            self._count = int(res['count'])

        return self._count

    def all(self):
        """
        Get all entities matching the current query in an array.
        
        Warning: This may result in an unbounded number of API calls! If the
        result set may be large (e.g., contacts or messages), consider using hasNext() / next()
        instead.
        
        Returns:
            array
        """

        return [item for item in self]

    def hasNext(self):
        """
        Returns true if there are any more entities in the result set, false otherwise
        
        Returns:
            bool
        """
        if self._limit is not None and self.offset >= self._limit:
            return False

        if self.data is None:
            self.loadNextPage()

        if self.pos < len(self.data):
            return True

        if not self.truncated:
            return False

        self.loadNextPage()
        return self.pos < len(self.data)

    def next(self):
        """
        Returns the next entity in the result set.
        
        Returns:
            Entity
        """
        if self._limit is not None and self.offset >= self._limit:
            raise StopIteration

        if (self.data is None) or (self.pos >= len(self.data) and self.truncated):
            self.loadNextPage()

        if self.pos < len(self.data):
            item_data = self.data[self.pos]
            self.pos += 1
            self.offset += 1
            cls = self.item_cls
            return cls(self.api, item_data, True)
        else:
            raise StopIteration

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def loadNextPage(self):
        request_params = self.params.copy()

        if self.next_marker is not None:
            request_params['marker'] = self.next_marker

        if self._limit is not None and not ("page_size" in request_params):
            request_params["page_size"] = min(self._limit, 200)

        response = self.api.doRequest("GET", self.path, request_params)

        self.data = response['data']
        self.truncated = response['truncated']
        self.next_marker = response['next_marker']
        self.pos = 0