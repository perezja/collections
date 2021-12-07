import re
import json

from object import Object
from uri import URI
from parts import NamePart, IdPart
from typing import TypeVar, Optional, Iterable, Mapping, List
from common import Record

from collections import defaultdict
from collections import namedtuple
from collections.abc import Mapping

T = TypeVar("T")

class Index:
    """Groups bucket into a mapping of indices to object list"""

    slots = ()

    def __get__(self, obj: Iterable[Object], cls=None):
        if obj is None:
            return self

        index = defaultdict(list) 
        for item in obj:
            index[item.id].append(item.name)  

        return index
    
class Groups():
    slots = ()

    Field = namedtuple('Field', 'name pattern regex')

    def __set__(self, obj, value: Mapping[str, str]):
        setattr(obj, '_groups', list())

        for field_name, pattern in value.items():
            _field = self.Field(field_name, pattern, re.compile(pattern))
            obj._groups.append(_field)

    def __get__(self, obj, cls=None):
        if obj is None or not hasattr(obj, '_groups'):
            return self
        
        #groups = defaultdict(list)
        groups = defaultdict(dict)

        for grp in obj._groups:
            for idx, dlist in obj.index.items():
                matches = list(map(lambda x: grp.regex.match(x), dlist))
                if not any(matches):
                    #groups[idx].append((grp.name, None))
                    groups[idx][grp.name] = None
                    continue

                if sum(isinstance(x, re.Match) for x in matches) > 1:
                    raise RuntimeError("Scalar field '{}' matched multiple objects for index '{}'".format(grp.name, idx))

                value = list(filter(bool, matches)).pop().string
                #groups[idx].append({grp.name, value))
                groups[idx][grp.name] = value

        return groups 

class Bucket:
    """An object bucket"""
    slots = ("_data", "_groups")

    # collection
    _data: List[Object] = list()

    # factory for collection items
    _Object = Object

    # feature interfaces
    source = URI
    index = Index()
    groups = Groups()
    
    def __init__(self, name: str, source: URI, id_pattern: str, *, groups: Optional[Mapping[str, str]], flt: Optional[Mapping[str, T]]=None): 
        self._Object.set_parameters(pattern=id_pattern, flt=flt)
        self.name = name 
        self.source = source
        self.groups = groups

    def __call__(self, data: Record):
        self._store(data)

    def __len__(self):
        return(len(self.index))

    def _store(self, data: Record):
        if data is None:
            return

        obj = self._Object(self.source, data)

        #setattr(obj, 'uri', self.uri.resolve(obj.name))
        self._data.append(obj)

    def __iter__(self):
        return(iter(self._data)) 

    def __repr__(self):
        return "{}('{}', len={}, items={})".format(
            self.__class__.__name__,
            self.name,
            len(self),
            str(self)
            )

    def __str__(self):
        sample = list(self.index.keys())[:3]

        d = self.groups if hasattr(self, '_groups') else self.index 
        d = { k:v for k,v in d.items() if k in sample }

        return json.dumps(d, indent=2)[:-2] + ",\n  ...\n}"

class Collection(Mapping):
    """Collection of buckets"""

    __slots__ = ('_buckets')

    name = NamePart()
    id = IdPart()

    def __init__(self):
        self._buckets = {}

    def __getitem__(self, key: str):
        return self._buckets[self._keytransform(key)]

    def __setitem__(self, key: str, value: Bucket):
        self._buckets[self._keytransform(key)] = value

    def keys(self):     # Mapping 
        return self._buckets.keys()

    def items(self):    # Mapping
        return self._buckets.items() 

    def values(self):   # Mapping
        return self._buckets.values()

    def get(self, index, default=None):     # Mapping 
        return self._buckets

    def __contains__(self, value: str):
        """Check if index is included"""
        return value in self.buckets.keys()


