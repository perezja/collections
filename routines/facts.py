from typing import Iterable, Mapping, List, Tuple   
from parts import T, ProxyPart, Properties
from fnmatch import fnmatch
# standard resource fact parts (RFC 3659, Section 7.5)
# note: lang, media-type and charset are excluded

class NamePart(ProxyPart):
    __slots__ = ('glob')

    __params__ = ('identity', 'glob')

    attribute = '_name'

    def valid(self, value):

        if self.identity:
            return super().valid(value)
        if self.glob:
            print("NamePart.valid: val={}, glob={}, res={}".format(value, self.glob, fnmatch(value, self.glob)))
            return fnmatch(value, self.glob)
        return True

class SizePart(ProxyPart):
    __slots__ = ('minsize', 'maxsize')

    __params__ = ('minsize', 'maxsize')

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


