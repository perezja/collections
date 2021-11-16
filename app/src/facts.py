from typing import TypeVar, Mapping, List, Tuple   
from parts import ProxyPart
# standard resource fact parts (RFC 3659, Section 7.5)
# note: land, media-type and charset are excluded

T = TypeVar('T')

class NamePart(ProxyPart):
    __slots__ = ()

    attribute = '_name'

class SizePart(ProxyPart):
    __slots__ = ()

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

class FactPart: 
    """Base object for all facts about the resource item"""

    __slots__ = ('facts')

    def __init__(self, facts):
        self.facts = facts 
    
    def __get__(self, obj, cls=None) -> List[Tuple[str, T]]:

        components = list()

        for fact in self.facts:
            value = getattr(obj, fact)
            proxy = getattr(cls, fact)
        
            components.append((fact, proxy.render(obj, value)))
        
        return components 
    
    def __set__(self, obj, mapping: Mapping[str, T]):

        for part in obj.__slots__:
            setattr(obj, part, None)

        for fact in self.facts: 
            value = mapping.get(fact)
            if value:
                setattr(obj, fact, value)

class Facts:
    """Base object for resource items"""
    __slots__ = ('_size', '_type', '_modify', '_create', '_perm', 'uri')
    __facts__ = ('size', 'type', 'modify', 'create', 'perm')

    # Scalar Parts
    size:int = SizePart()
    type:str = TypePart()
    # TODO: render `modify` and `create` into date types
    modify:str = ModifyPart()
    create:str = CreatePart()
    perm:str = PermPart()

    # Compound Interfaces
    facts = FactPart(__facts__)

    def __set__(self, obj, value: Mapping[str, T]):
        self.facts = value 
    def __get__(self, obj, cls):
        return self.facts 



