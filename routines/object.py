from parts import T, PathPart, NamePart, IdPart, URIPart, SizePart, TypePart, ModifyPart, CreatePart, PermPart
from typing import Optional, Set, Mapping, Iterable, Tuple
from uri import URI

import re

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

class Filter:
    """Defines the mappable domain for all object properties which may be set by a bucket filter"""
    __slots__ = ()

    def __set__(self, obj, flt: Mapping[str, T]):
        print("Filter.__set__: self={}, obj={}".format(self, obj))
        self.reset(obj)

        supp=self.parse(obj, flt)
        
        for bounds in supp:
            part, params = bounds
            if part not in obj.__parts__:
                raise AttributeError("{0.__class__.__name__}.{1} is not defined".format(obj, part))
            proxy = getattr(obj.__class__, part)

            for param, val in params.items():
                if param not in proxy.__filters__:
                    raise AttributeError("{0.__class__.__name__}.{1.__class__.__name__} is not parameterized by '{2}'".format(obj, proxy, param))
                print("Filter.__set__: setting {}.{} to {}".format(proxy, param, val))
                setattr(proxy, param, val)

    def __get__(self, obj, cls=None) -> Iterable[Tuple[str, Mapping[str, T]]]:
        if obj is None:
            return self

        filter = list() 

        if not obj.__parts__: return None 
        for part in obj.__parts__:
            bounds = {} 
            proxy = getattr(cls, part)

            for param in proxy.__filters__:
                if hasattr(proxy, param):
                    value = getattr(proxy, param)
                    if value: bounds[param] = value 

            if bounds: filter.append((part, bounds))

        return filter 

    def parse(self, obj, flt: Mapping[str, T]) -> Iterable[Tuple[str, Mapping[str, T]]]:
        """filter arguments not mapping to a property parameter are ignored"""

        model = obj.model()
        print(model)

        _filter = list()
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

                _filter.append((prop, pmap))

        return _filter 

    def reset(self, obj):
        print("Object.reset_filter: cls={}".format(cls))
        for part in obj.__parts__:
            proxy = getattr(obj.__class__, part)
            proxy.reset() 

class Masked:
    __slots__ = ()

    def __get__(self, obj, cls=None):
        print("Masked.__get__: self={}, obj={}, cls={}".format(self, obj, cls))
        bools = list()
        for part in obj.__parts__:
            proxy = getattr(cls, part) 
            bools.append(proxy.defined(obj))

        print("Masked.__get__: bool vector={}".format(bools))
        return not all(bools)

class Object:
    """Atomic units of workflow inputs"""
    __slots__ = ('source', '_path', '_size', '_type', '_modify', '_create', '_perm') # properties

    __parts__ = ('relpath', 'size', 'type', 'modify', 'create', 'perm')

    # scalar fact parts
    name: str      = NamePart()
    relpath: str   = PathPart()
    uri: str       = URIPart()
    id: str        = IdPart()
    size: int      = SizePart()
    type: str      = TypePart()
    modify: str    = ModifyPart()
    create: str    = CreatePart()
    perm: str      = PermPart() 

    # uri interface
    source: URI 
    uri: URIPart()

    # compound interfaces
    properties  = Properties()

    # feature interface 
    filter = Filter()
    masked = Masked() 

    def __new__(cls, source: URI, data: Tuple[str, Mapping[str, T]]):

        obj = super(Object, cls).__new__(cls)

        relpath, mapping = data 
        mapping['relpath'] = relpath 

        obj.properties = mapping 
        obj.source = source

        return obj
    
    def __str__(self):
        props = ",".join("{}={}".format(part, value) for part, value in self.properties)
        return "Object({})".format(props)

    def __link__(self):
        pass

    @classmethod
    def model(cls) -> Mapping[str, Set]:
        """A model is the parameterization for each property"""
        model = {}
        if not cls.__parts__: return None 
        for part in cls.__parts__:
            proxy = getattr(cls, part)
            model[part] = proxy.__filters__ 

        return model 

    @classmethod
    def set_parameters(cls, *, pattern: str, flt: Optional[Mapping[str, T]]):
        print("Object.set_parameters: cls={}, pattern={}".format(cls, pattern))
        cls._regex = re.compile(pattern)
        
        if flt: cls._filter = flt


