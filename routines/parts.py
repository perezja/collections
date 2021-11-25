from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Mapping, Set, Iterable, Tuple, Optional, Any 

T = TypeVar("T")

# https://github.com/marrow/uri/blob/develop/uri/part/base.py
class Part:
    """Descriptor protocol for sets of standard resource fact parts (RFC 3659, Section 7.5)"""
    
    __slots__ = ()
    
    empty = None 

    def flush(self):
        for param in self.__params__:
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

    __params__ = ('identity',) 
    
    attribute: str = None

    cast: T = str

    def __init__(self):
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

class Mask:
    __slots__ = ()

    def __get__(self, obj, cls=None):
        print("Mask.__get__: self={}, obj={}, cls={}".format(self, obj, cls))
        bools = list()
        for part in obj.__parts__:
            proxy = getattr(cls, part) 
            bools.append(proxy.defined(obj))

        print("Mask.__get__: bool vector={}".format(bools))
        return not all(bools)

class Support:
    """Defines the mappable domain for all object properties which may be set by a bucket filter"""
    __slots__ = ()

    def __set__(self, obj, flt: Mapping[str, T]):
        print("Support.__set__: self={}, obj={}".format(self, obj))
        obj.flush()

        supp=self.parse_filter(obj, flt)
        
        for bounds in supp:
            part, params = bounds
            if part not in obj.__parts__:
                raise AttributeError("{0.__class__.__name__}.{1} is not defined".format(obj, part))
            proxy = getattr(obj.__class__, part)

            for param, val in params.items():
                if param not in proxy.__params__:
                    raise AttributeError("{0.__class__.__name__}.{1.__class__.__name__} is not parameterized by '{2}'".format(obj, proxy, param))
                print("Support.__set__: setting {}.{} to {}".format(proxy, param, val))
                setattr(proxy, param, val)

    def __get__(self, obj, cls=None) -> Iterable[Tuple[str, Mapping[str, T]]]:
        if obj is None:
            return self

        support = list() 
        if not obj.__parts__: return None 
        for part in obj.__parts__:
            bounds = {} 
            proxy = getattr(cls, part)

            for param in proxy.__params__:
                if hasattr(proxy, param):
                    value = getattr(proxy, param)
                    if value: bounds[param] = value 

            if bounds: support.append((part, bounds))

        return support 

    @classmethod
    def parse_filter(cls, obj, flt: Mapping[str, T]) -> Iterable[Tuple[str, Mapping[str, T]]]:
        """filter arguments not mapping to a property parameter are ignored"""

        model = obj.model()
        print(model)

        support = list()
        for prop, params in model.items():
            # filter can include scalar property (i.e., type="dir", name="file.txt")
            pset = set(params) 
            if 'identity' in pset:
                pset.remove('identity'); pset.add(prop)

            defined = set(flt).intersection(pset) 

            if defined:
                pmap = {param: val for param, val in flt.items() if param in defined}
                if prop in defined: 
                    pmap['identity'] = pmap[prop]; del pmap[prop]

                support.append((prop, pmap))

        return support

class Properties:
    "Compound interface for all object properties"
    __slots__ = ()
    __parts__ = ()

    def __get__(self, obj, cls=None) -> Iterable[Tuple[str, T]]:
        if obj is None:
            return self

        components = list()

        for part in obj.__parts__:
            value = getattr(obj, part)
            proxy = getattr(cls, part)
        
            components.append((part, proxy.render(obj, value))) 

        return components 


    def __set__(self, obj, mapping: Mapping[str, T]):

        for part in obj.__slots__:
            setattr(obj, part, None)

        for part in obj.__parts__: 
            value = mapping.get(part)
            if value:
                setattr(obj, part, value)
   
