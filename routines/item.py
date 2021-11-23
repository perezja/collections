from ftp import FTPConnection
from uri import URI
from typing import Mapping, Tuple, List 
from facts import T, Facts  
from collections import namedtuple

class Object:
    """Atomic units of workflow inputs"""
    __slots__ = ('name', 'uri')

    name: str
    uri: str

    properties = Facts()

    def __init__(self, record: Tuple[str, Mapping[str, T]]):
        self.name, facts = record 
        self.properties = facts

    @classmethod
    def set_model(cls, model: Tuple[str, Mapping[str, T]]):
        scalar, params = model
        if scalar not in cls.__facts__:
            raise AttributeError("{0.__name__}.{} is not defined".format(cls, scalar))

        proxy = getattr(cls, scalar)

        for param, val in params.items():
            if proxy.in_scope(param):
                setattr(cls, param, val)
            else:
                raise AttributeError("{0.__name__}.{1.__name__} is not parameterized by '{2}'".format(cls, proxy, param))


class Bucket:
    """An object bucket"""

    _items: List[Tuple[str, Object]] = list() 

    def __init__(self, base:str, auth:Mapping): 
        print(auth)
        self.uri = URI(_uri=base, **auth)  
        print("Bucket.__init__(): {}".format(self.uri))
        print("Bucket.__init__(): scheme={}, auth={}".format(self.uri.scheme, self.uri.authority))

    def __call__(self, obj:Object):
        self._store(obj)

    def __len__(self):
        return(len(self._items))

    def _store(self, obj:Object=None):
        if obj is None:
            return

        setattr(obj, 'uri', self.uri.resolve(obj.name))
        self._items.append(obj)

    def __iter__(self):
        return(iter(self._items)) 

if __name__ == "__main__":

    record=[('.', {'modify': '20200526174446', 'perm': 'fle', 'size': '0', 'type': 'cdir', 'unique': 'EBU3F4D43B', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'}), ('..', {'modify': '20211108212254', 'perm': 'fle', 'size': '40', 'type': 'pdir', 'unique': 'EBU1', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'}), ('integrated_sv_map', {'modify': '20150619134953', 'perm': 'fle', 'size': '0', 'type': 'dir', 'unique': 'EBU4A0F18F', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'}), ('data', {'modify': '20200526174446', 'perm': 'fle', 'size': '0', 'type': 'dir', 'unique': 'EBU3F4D43C', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'})]


