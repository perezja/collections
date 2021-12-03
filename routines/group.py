class Group:
    """A group of related data"""

    slots = ("_id", "_data")

    name  = NamePart() 
    id    = IDPart()
    index = Index()

