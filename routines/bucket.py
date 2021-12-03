from object import Object
from typing import TypeVar, Optional, Mapping, List
from common import Record

from collections import defaultdict

T = TypeVar("T")

class Index:
    """Groups bucket into a mapping of indices to object list"""

    slots = ()

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        index = defaultdict(list) 
        for item in obj:
            index[item.id].append(item.name)  

        return index

class Bucket:
    """An object bucket"""
    slots = ("_data")

    _data: List[Object] = list()
    _Object = Object

    index = Index()
    
    def __init__(self, pattern: str, *, flt: Optional[Mapping[str, T]]=None): 
        self._Object.set_parameters(pattern=pattern, flt=flt)

    def __call__(self, data: Record):
        self._store(data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return(len(self._items))

    def _store(self, data: Record):
        if data is None:
            return

        obj = self._Object(data)

        #setattr(obj, 'uri', self.uri.resolve(obj.name))
        self._data.append(obj)

    def __iter__(self):
        return(iter(self._data)) 

"""
class Patterns:
    slots = ('_patterns') 

    def __init__(self):
        self._patterns = {
                'index': None,
                'groups': {}
        }

    @property
    def index:
        return self._patterns['index']

    @index.setter
    def index(self, value)
        self._patterns['index'] = value

    @property
    def groups:
        return self._patterns['groups']

    @groups.setter
    def groups(self, mapping: Mapping[str, str])
    
        group_name = mapping.key
        self._patterns['groups'][group_name] = mapping.value 
"""

