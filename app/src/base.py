from typing import Mapping, List, Tuple, Iterable 

class FactPart: 
    """Base object for all facts about the resource item"""

    __slots__ = ('facts')

    def __init__(self, facts):
	self.facts = facts 
	
    def __get__(self, obj, cls=None) -> List[Tuple[str, T]]:

	for part in self.facts:
            value = getattr(obj, fact)
	    fact = getattr(cls, fact)
		
	    components.append((fact.render(obj, value))
		
	return components 
	
    def __set__(self, obj, mapping: Mapping[str, T]):
	for part in obj.__slots__:
	    setattr(obj, part, None)

	for fact in self.facts: 
	    value = getattr(mapping, fact)
		if value:
	 	    setattr(obj, fact, value)
