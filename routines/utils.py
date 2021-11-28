#pyre-strict
import os
import fnmatch

from plugins import ProtocolInterface
from common import T, Record, Mapping, Tuple, List 
import fnmatch
import re

class Walker:

    def __init__(self, pcl: ProtocolInterface):
        self.pcl = pcl
        self._prog = None

    def scandirs(self, pathname, rgx=None, *, cache=True) -> List[str]:
        """for a given pathname, perform shell-like expansion on the basename 
        and return all paths, optionally performing regular expression matching 
        on the directory names if provided
        """
        if rgx:
            prog = self._prog
            if cache and not prog: 
                print("Walker.scandirs: compiling and caching regex '{}'".format(rgx))
                prog = re.compile(rgx)
                self._prog = prog
    
            elif not cache:
                prog = re.compile(rgx) 
    
        results = list()
        for path in self.glob(pathname, fullpath=True):
            print("Walker.scandirs: searching {}".format(path))
            for dirname in self._listdir(path):
                res = os.path.join(path, dirname)
                if not rgx or prog.match(dirname):
                    results.append(res)

        return results
                 

    def glob(self, pathname, fullpath=False):
        root, basename = os.path.split(pathname)
        names = self._listdir(root)
        names = fnmatch.filter(names, basename)
        if fullpath:
            return [os.path.join(root, name) for name in names]

        return names 

    def _rlistdir(self, dirname):
        names = self._listdir(dirname)
        for x in names:
            yield x
            path = os.path.join(dirname, x) if dirname else x
            for y in self._rlistdir(path):
                yield os.path.join(x, y)

    def _listdir(self, path) -> str:
        return [dirname for dirname, facts in self.pcl.ls(path) if self._isdir(facts)]

    def _isdir(self, facts: Mapping[str, T]):
        return facts.get('type')=='dir'

