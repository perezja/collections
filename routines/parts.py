import os

from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Mapping, Set, Iterable, Tuple, Optional, Any 

from fnmatch import fnmatch
from pathlib import Path

T = TypeVar("T")

# https://github.com/marrow/uri/blob/develop/uri/part/base.py
class Part:
    """Descriptor protocol for sets of standard resource fact parts (RFC 3659, Section 7.5)"""
    
    __slots__ = ()
    
    empty = None 

    def reset(self):
        for param in self.__filters__:
            setattr(self, param, None)

    def render(self, obj, value, raw:bool=False):
        if not value: return self.empty
        return value

    def valid(self, value) -> bool:
        ans = True

        if self.identity:
            print('Part.valid: {}=={} is {}'.format(value, self.identity, value==self.identity))
            ans = (value==self.identity)

        return ans

    def defined(self, obj) -> bool:
        if not hasattr(obj, self.attribute):
            return True

        value = getattr(obj, self.attribute)
        return self.valid(value)

class ProxyPart(Part):
    __slots__ = ('identity')

    __filters__ = ('identity',) 
    __params__ = ()
    
    attribute: str = None

    cast: T = str

    def __init__(self):
        for param in self.__filters__:
            setattr(self, param, None)

        for param in self.__params__:
            setattr(self, param, None)
    
    def __get__(self, obj, cls=None):
        if obj is None: 
            return self

        return getattr(obj, self.attribute)
    
    def __set__(self, obj, value: Optional[T]):
        if value == b'':
            value = None
        
        if value is not None:
            value = self.cast(value)
        
        setattr(obj, self.attribute, value)

# standard resource fact parts (RFC 3659, Section 7.5)
# note: lang, media-type and charset are excluded

class PathPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_path'
	cast = Path
	empty = '/'

class NamePart(ProxyPart):
    __slots__ = ('glob')

    __filters__ = ('identity', 'glob')

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        return obj.relpath.name 

    def valid(self, value):

        if self.identity:
            return super().valid(value)
        if self.glob:
            print("NamePart.valid: val={}, glob={}, res={}".format(value, self.glob, fnmatch(value, self.glob)))
            return fnmatch(value, self.glob)
        return True

class IdPart:
    __slots__ = ()

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        if not hasattr(obj, '_regex'):
            return obj.name

        print("IdPart.__get__: obj={}, cls={}, obj.name={}".format(obj, cls, obj.name))
        match = obj._regex.match(os.path.basename(obj.name)) 
        if match:
            return match.group(0)

        return obj.name 

class URIPart(ProxyPart):
    __slots__ = ()

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        return obj.source.resolve(obj.relpath)


class PatternPart(ProxyPart):
    __slots__ = ('pattern')

    attribute = '_pattern'


class SizePart(ProxyPart):
    __slots__ = ('minsize', 'maxsize')

    __filters__ = ('minsize', 'maxsize')

    attribute = '_size' 

    cast: T = int

    def valid(self, value):
        ans = True

        if self.minsize:
            print("{} > (minsize={}) is {}".format(value, self.minsize, value>self.minsize)) 
            ans = value>self.minsize
            
        if self.maxsize:
            print("{} < (maxsize={}) is {}".format(value, self.maxsize, value<self.maxsize)) 
            ans = (value<self.maxsize) and ans

        return ans

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


