#pyre-strict
import os

from plugins import ProtocolInterface
from common import T, Record 

class Walker:

    def __init__(self, pcl: ProtocolInterface):
        self.pcl = pcl

    def _rlistdir(self, dirname):
        names = self._listdir(dirname)
        for x in names:
            yield x
            path = os.path.join(dirname, x) if dirname else x
            for y in self._rlistdir(path):
                yield os.path.join(x, y)

    def _listdir(self, pathname) -> str:
        print("Walker._listdir: pathname={}".format(pathname))
        return [dirname for dirname, facts in self.pcl.ls(pathname) if self._isdir(facts)]

    def _isdir(self, facts: Mapping[str, T]):
        return facts.get('type')=='dir'

