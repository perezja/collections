from bucket import Bucket

class Collection:
    """Collection of buckets"""


    __slots__ = ('_buckets')

    def __init__(self):
        self.buckets = {}

    def 

    def __contains__(self, value: str):
        """Check if index is included"""
        return value in self.buckets.keys()

