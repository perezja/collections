#pyre-strict
"""
Storage servers and downloading handlers for parameterizing collections
"""

from abc import ABC, abstractmethod
from typing import NewType, Final, Dict, Mapping, Callable
from error import ImportError

URI_SCHEMA: Final = ("ftp") 

# Association of a file name with a standard set of facts about the file (Extensions to FTP, RFC 3659)
FileFacts = tuple[str, dict] 

class URI:
    def __init__(self, uri: str, scheme: str, facts: dict) -> None:
        """
        URI is a fully qualified path sufficient for file retrieval
        """
        if scheme not in URI_SCHEMA:
            raise error.ImportError(uri_type + " URI type not suppported") 

        self.uri = uri
        self.handler = _get_download_handler(uri_scheme)

    def __bool__(self) -> bool:
        return(self._is_accessible())

    def handler() -> DownloadHandler:
        return _get_download_handler(uri_scheme)

    def _is_accessible() -> bool:
        """
        tests connection to URI provider and the accessibility of the resource
        """
   
class DownloadHandler(ABC):
    """
    Download handler for populating a Collection
    """

    def __init__(self, uri_scheme: ) -> None:

class HandlerConnection(ABC):
    """
    Connection for a DownloadHandler 
    """

    def __init__(self, host: str, auth: Crendentials) -> None:
        self.host = host
        self.failed_attempts = 0
        self.max_attempts = 5
        self.stop_when_connected()

    @abstractmethod
    def _connect(self) -> None:
        raise NotImplementedError

    def stop_when_connected(self)
        """
        continually try to reconnect ad infinitum

        try:
            self._connect()
        except ConnectionError:
            logging.warning("CONNECT {} FAILED; trying again...".format(self.host))
            time.sleep(...)
            self.stop_when_connected()
        """

class Credentials(ABC):
    """
    Credentials for accessing storage server volume data
    """
    def __init__(self, user: str = "anonymous", passwd: str = None):
        self.user = user
        self.passwd = passwd
 




class StorageServer(ABC):
    """
    Storage server hosting a data collection
    """

    def __init__(self, host: str, auth: Credentials):

##############################################################################
# handlers
##############################################################################

def _get_download_handler(uri_scheme) -> DownloadHandler:
    pass

class FTPHandler(DownloadHandler):

##############################################################################
# connections 
##############################################################################


