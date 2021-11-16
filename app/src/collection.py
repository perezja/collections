#pyre-strict
"""
Collections object for sequencing data
"""

from WDL.Type import File, Directory 
from collections.abc import Collection 


class Collection(collections.abc.Collection):
    """
    A collection of related data which are uniform in file type and are processed in an analysis group. Each item of the collection is indexed by an idenitifier (e.g., SampleID) which can be mapped to other collections of related sequencing data. 
    """

    def __init__(self, index_file: File, root: Directory):
        self._index_source = index_file 
        self._root_source = root

if __name__ == "__main__":


    c = 

