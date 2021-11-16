from ftp import FTPConnection
from uri import URI
from typing import Mapping, Tuple, List 
from facts import T, Facts  
from collections import namedtuple

class Object:
    """Base object for a resource (i.e., Collection, Bucket, Item)"""
    __slots__ = ('name', 'uri')

    facts = Facts()

    def __init__(self, record: Tuple[str, Mapping[str, T]]):
        self.name, _facts = record 
        self.facts = _facts

class Bucket:
    """Resource bucket"""

    _items: List[Tuple[str, Object]] = list() 

    def __init__(self, base:str, auth:Mapping): 
        print(auth)
        self.uri = URI(_uri=base, **auth)  
        print("Bucket.__init__(): {}".format(self.uri))
        print("Bucket.__init__(): scheme={}, auth={}".format(self.uri.scheme, self.uri.authority))

    def __call__(self, obj:Object):
        self._store(obj)

    def __len__(self):
        return(len(self._items))

    def _store(self, obj:Object=None):
        if obj is None:
            return

        setattr(obj, 'uri', self.uri.resolve(obj.name))
        self._items.append(obj)

    def __iter__(self):
        return(iter(self._items)) 

if __name__ == "__main__":

    import argparse
    import json
    
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('--loglevel', default='INFO')
    args = parser.parse_args()
    
    with open(args.config, 'r') as ip:
        config = json.loads(ip.read())

    Auth = namedtuple('Auth', 'user password host port')

    path = config['path']
    user = "anonymous" if "host" in config else config["host"] 
    port = None if not "port" in config else int(config["port"]) 
    passwd = None if not "passwd" in config else config["passwd"] 

    auth = Auth(user=user, password=passwd, host=config["host"], port=port) 
    cred = auth._asdict()
    bucket = Bucket(path, cred)
    
    ftp = FTPConnection(config['host'], config['ftp_list_method'])    
    results = ftp.process_path(config['path'])
    for result in results:
        item = Object(record=result)
        bucket(item)
    print("Bucket of size {}".format(len(bucket)))
    for item in bucket:
        print("name={}, facts={}, uri={}".format(item.name, item.facts, item.uri))
 

        


