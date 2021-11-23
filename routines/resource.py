from traceback import format_exc 
from typing import Tuple

class Conn:
    """
    Abstraction of client connection to the storage server
    """

    def __init__(self, host, errors=None):
        self.host = host
        self.failed_attempts = 0
        self.max_attempts = 5
        self.stop_when_connected()

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    def stop_when_connected(self):
        try:
            self.connect()
        except Exception as e:
            logging.error(format_exc(e))

class FTPPlugin:

       #logging.info("CONNECT {} ATTEMPT".format(self.host))

class Handler(Conn):
    def process_path(path: str):
        pass

    def ls(self):

    def crawl():
        pass

class Resource:
    """Data source for building a collection of buckets"""

    # source is root directory from which all buckets are derived
    __slots__ = ("_source")


class Factory:

    def _create_bucket():
        pass
    def _create_collection():
        pass

