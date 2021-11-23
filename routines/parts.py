from abc import ABC, abstractmethod
from typing import TypeVar, Mapping, Set, Iterable, Tuple, Optional, Any 

T = TypeVar("T")

# https://github.com/marrow/uri/blob/develop/uri/part/base.py
class Part:
    """Descriptor protocol for sets of standard resource fact parts (RFC 3659, Section 7.5)"""
    
    __slots__ = ()
    
    empty = None 
    
    def render(self, obj, value, raw:bool=False):
        if not value: return self.empty
        return value

    def valid(self, obj) -> bool:
        paramset=self.paramset
        print("Part.valid: {}.paramset={}".format(self, paramset))
        for param in paramset:
            value = getattr(obj, param)
            print("Part.valid: {}.{}={}".format(obj, param, value))
        return True

    def in_scope(self, param):
        if param in self.paramset: return True
        else: return False

class ProxyPart(Part):
    __slots__ = ('identity',)

    __params__ = ('identity',) 
    
    attribute: str = None
    cast = str
    
    def __get__(self, obj, cls=None):
        print("ProxyPart.__get__: self={}, obj={}, cls={}".format(self, obj, cls))
        if obj is None: return self
        return getattr(obj, self.attribute)
    
    def __set__(self, obj, value: Optional[T]):
        if value == b'':
            value = None
        
        if value is not None:
            value = self.cast(value)
        
        setattr(obj, self.attribute, value)

class GroupPart: 
    """Descriptor for conceptually grouped slots in the owner class"""

    __slots__ = ('parts')

    def __init__(self, parts):
        self.parts = parts 
    
    def __get__(self, obj, cls=None) -> Iterable[Tuple[str, T]]:
        print("GroupPart.__get__: self={}, obj={}, cls={}".format(self, obj, cls))

        components = list()

        for part in self.parts:
            print("GroupPart.__get__: processing {}".format(part))
            value = getattr(obj, part)
            print("GroupPart.__get__: got {} from {}.{}".format(value, obj, part))
            proxy = getattr(cls, part)
            print("GroupPart.__get__: got {} from {}.{}".format(proxy, cls, part))
        
            components.append((part, proxy.render(obj, value))) 
            print("GroupPart.__get__: calling {}.render({}, {})".format(proxy, obj, value))

        return components 
    
    def __set__(self, obj, mapping: Mapping[str, T]):
        print("In GroupPart.__set__: self={}, obj={}, mapping={}".format(self, obj, mapping))

        for part in self.parts: 
            value = mapping.get(part)
            if value:
                setattr(obj, part, value)

class Properties:
    "Base class for all object properties"
    __slots__ = ()
    __parts__ = ()

    #def __init__(self, model: Mapping[str, T], support: Tuple[str, Mapping[str, T]]=None);

    def __get__(self, obj, cls=None) -> Iterable[Tuple[str, T]]:
        print("Properties.__get__: self={}, obj={}, cls={}".format(self, obj, cls))
        if obj is None:
            return self

        components = list()

        for part in obj.__parts__:
            print("Properties.__get__: processing {}".format(part))
            value = getattr(obj, part)
            print("Properties.__get__: got {} from {}.{}".format(value, obj, part))
            proxy = getattr(cls, part)
            print("Properties.__get__: got {} from {}.{}".format(proxy, cls, part))
        
            components.append((part, proxy.render(obj, value))) 
            print("Properties.__get__: calling {}.render({}, {})".format(proxy, obj, value))

        return components 


    def __set__(self, obj, mapping: Mapping[str, T]):
        print("Properties.__set__: self={}, obj={}, mapping={}".format(self, obj, mapping))

        for part in obj.__slots__:
            setattr(obj, part, None)

        for part in obj.__parts__: 
            value = mapping.get(part)
            if value:
                setattr(obj, part, value)

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
    def set_support(cls, support: Iterable[Tuple[str, Mapping[str, T]]]):
        print("Properties.set_support: cls={}".format(cls))
        
        for bounds in support:
            part, params = bounds
            if part not in cls.__parts__:
                raise AttributeError("{0.__name__}.{1} is not defined".format(cls, part))
            proxy = getattr(cls, part)

            for param, val in params.items():
                if param not in proxy.__params__:
                    raise AttributeError("{0.__name__}.{1.__class__.__name__} is not parameterized by '{2}'".format(cls, proxy, param))
                setattr(proxy, param, val)
    @classmethod
    def get_support(cls) -> Iterable[Tuple[str, Mapping[str, T]]]:

        support = list() 
        if not cls.__parts__: return None 
        for part in cls.__parts__:
            bounds = {} 
            proxy = getattr(cls, part)

            for param in proxy.__params__:
                if hasattr(proxy, param):
                    bounds[param] = getattr(proxy, param)

            if bounds: support.append((part, bounds))

        return support 


