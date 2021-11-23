from typing import TypeVar, Iterable, Mapping, List, Tuple   
from parts import ProxyPart, GroupPart, Properties
# standard resource fact parts (RFC 3659, Section 7.5)
# note: lang, media-type and charset are excluded

T = TypeVar('T')

class NamePart(ProxyPart):
    __slots__ = ('glob')

    __params__ = ('glob')

    attribute = '_name'

class SizePart(ProxyPart):
    __slots__ = ('minsize', 'maxsize')

    __params__ = ('minsize', 'maxsize')

    attribute = '_size' 
    cast = int

class TypePart(ProxyPart):
    __slots__ = ()

    attribute = '_type'

class ModifyPart(ProxyPart):
    __slots__ = ()

    attribute = '_modify'

class CreatePart(ProxyPart):
    __slots__ = ()

    attribute = '_create'

class PermPart(ProxyPart):
   __slots__ = ()

   attribute = '_perm'

class Facts(Properties):
    """Object properties"""
    __slots__ = ('_size', '_type', '_modify', '_create', '_perm')
    __parts__ = ('size', 'type', 'modify', 'create', 'perm')

    # Scalar Parts
    size:int = SizePart()
    type:str = TypePart()
    # TODO: render `modify` and `create` into date types
    modify:str = ModifyPart()
    create:str = CreatePart()
    perm:str = PermPart()

#    def __set__(self, obj, mapping):
#        print("Facts.__set__: self={}, obj={}, mapping={}".format(self, obj, mapping))
#        super(Facts, self).__set__(obj, mapping)
#    def __get__(self, obj, cls=None):
#        print("Facts.__get__: self={}, obj={}, mapping={}".format(self, obj, mapping))
#        super(Facts, self).__get__(obj, cls)
#
    size_params = ('size', {"minsize": 4000, "maxsize": 1241211})
    wrong_params1 = ('fins', {"minsize": 4000, "maxsize": 1241211})
    wrong_params2 = ('size', {"footsize": 4000, "maxsize": 1241211})
    records=[('.', {'modify': '20200526174446', 'perm': 'fle', 'size': '0', 'type': 'cdir', 'unique': 'EBU3F4D43B', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'}), ('..', {'modify': '20211108212254', 'perm': 'fle', 'size': '40', 'type': 'pdir', 'unique': 'EBU1', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'}), ('integrated_sv_map', {'modify': '20150619134953', 'perm': 'fle', 'size': '0', 'type': 'dir', 'unique': 'EBU4A0F18F', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'}), ('data', {'modify': '20200526174446', 'perm': 'fle', 'size': '0', 'type': 'dir', 'unique': 'EBU3F4D43C', 'unix.group': '0', 'unix.groupname': 'anonymous', 'unix.mode': '0444', 'unix.owner': '14', 'unix.ownername': 'ftp'})]

