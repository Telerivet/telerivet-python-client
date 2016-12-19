
class Entity(object):    
    def __init__(self, api, data, is_loaded = True):    
        self._api = api
        self._vars = None
        self._dirty = {}
        self._data = {}
        self._setData(data)
        self._is_loaded = is_loaded        
    
    def _setData(self, data):
        self._data = data
        
        if 'vars' in data:            
            self._vars = CustomVars(data['vars'])
        else:
            self._vars = CustomVars({})    
    
    def load(self):    
        if not self._is_loaded:
            self._is_loaded = True
            self._setData(self._api.doRequest('GET', self.getBaseApiPath()))            
            self._data.update(self._dirty)
        
    def __getattr__(self, name):    
        if name == 'vars':
            self.load()
            return self._vars
        
        data = self._data
        if name in data:
            return data[name]
        elif self._is_loaded:
            return None

        self.load()
        data = self._data

        if name in data:
            return data[name]

        return None
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
            return
            
        self._data[name] = value
        self._dirty[name] = value
    
    def save(self):
    
        dirty_props = self._dirty

        if self._vars is not None:
            dirty_vars = self._vars.getDirtyVariables()
            if len(dirty_vars) > 0:            
                dirty_props['vars'] = dirty_vars
            
        self._api.doRequest('POST', self.getBaseApiPath(), dirty_props)
        self._dirty = {}
        
        if self._vars is not None:
            self._vars.clearDirtyVariables()
    
    def __repr__(self):
        res = self.__class__.__name__
        if not self._is_loaded:
            res += " (not loaded)";

        import json
        res += " JSON: " + json.dumps(self._data)
        
        return res
    
    def getBaseApiPath(self):
        abstract

class CustomVars:
    def __init__(self, vars):
        self._vars = vars
        self._dirty = {}
    
    def all(self):
        return self._vars
    
    def getDirtyVariables(self):
        return self._dirty
    
    def clearDirtyVariables(self):
        self._dirty = {}
        
    def __getattr__(self, name):
        if name in self._vars:
            return self._vars[name]
        else:
            return None
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
            return
            
        self._vars[name] = value
        self._dirty[name] = value
