from abc import ABC, abstractmethod
from typing import TypeVar, Mapping, Iterable, Optional, Any 

T = TypeVar("T")

# https://github.com/marrow/uri/blob/develop/uri/part/base.py
class Part:
    """Descriptor protocol objects for some standard resource fact parts (RFC 3659, Section 7.5)"""
    
    __slots__ = ()
    
    empty = None 
    
    def render(self, obj, value, raw:bool=False) -> T:
        if not value: return self.empty
        return value
    
    @abstractmethod
    def __get__(self, obj, cls=None):
        pass
    
    @abstractmethod
    def __set__(self, obj, value) -> None:
        pass


class ProxyPart(Part):
    __slots__ = ()
    
    attribute = None
    cast = str
    
    def __get__(self, obj, cls=None):
        if obj is None: return self
        return getattr(obj, self.attribute)
    
    def __set__(self, obj, value: Optional[T]) -> None:
        if value == b'':
            value = None
        
        if value is not None:
            value = self.cast(value)
        
        setattr(obj, self.attribute, value)

class _GroupPart(Part):
    __slots__ = ()
    
    attributes:Iterable[str] = ()
    sep:str = ''
    
    def __get__(self, obj, cls=None) -> str:
        if obj is None: return self
        
        cls = obj.__class__
        attrs = (getattr(cls, attr).render for attr in self.attributes)
        values = (getattr(obj, attr) for attr in self.attributes)
        pipeline = (attr(obj, value) for attr, value in zip(attrs, values))
        
        return self.sep.join(i for i in pipeline if i)
    
    def __set__(self, obj, value: Mapping[str, T]):
        raise TypeError("{0.__class__.__name__} is not assignable.".format(self))
