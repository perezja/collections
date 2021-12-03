from ftp import FTPConnection
from uri import URI
from typing import Iterable, Mapping, Set, Tuple, List 
from facts import NamePart, SizePart, TypePart, ModifyPart, CreatePart, PermPart  
from parts import T, Properties, Support, Mask
from collections import namedtuple

class Object:
    """Atomic units of workflow inputs"""
    __slots__ = ('_uri', '_name', '_size', '_type', '_modify', '_create', '_perm') # properties

    __parts__ = ('name', 'size', 'type', 'modify', 'create', 'perm')

    # Scalar Parts
    name: str = NamePart()
    size:int = SizePart()
    type:str = TypePart()
    modify:str = ModifyPart()
    create:str = CreatePart()
    perm:str = PermPart()

    
    # Compound interfaces
    properties = Properties()
    support = Support()

    # Feature interface 
    masked = Mask() 

    def __new__(cls, data: Tuple[str, Mapping[str, T]], **kwargs):

        obj = super(Object, cls).__new__(cls)

        flt = kwargs.get('filter')
        if flt: obj.support = flt 
        
        name, mapping = data 

        mapping['name'] = name
        obj.properties = mapping 

        return obj

    @classmethod
    def factory(cls, flt: Mapping[str, T]=None) -> "Object":
        if not flt:
            return cls 

        cls.properties.support = supp
        return cls

    @classmethod
    def model(cls) -> Mapping[str, Set]:
        """A model is the parameterization for each property"""
        model = {}
        if not cls.__parts__: return None 
        for part in cls.__parts__:
            proxy = getattr(cls, part)
            model[part] = proxy.__params__ 

        return model 

    @classmethod
    def flush(cls):
        print("Object.flush: cls={}".format(cls))
        for part in cls.__parts__:
            proxy = getattr(cls, part)
            proxy.flush() 

class Group:
    """A group of related data"""

    slots = ("_id", "_data")

    name  = NamePart() 
    id    = IDPart()
    index = Index()

class Bucket:
    """An object bucket"""
    slots = ("_size", "_index", "_units", ")

    # compound interface
    items: List[Tuple[str, Object]] = list() 
    index = Index()
    units = GroupPart()

    def __init__(self, index_rgx=None): 
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


