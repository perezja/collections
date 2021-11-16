from typing import Optional

class ImportError(Exception):
    """
    Failure to load a resource
    """
    def __init__(self, uri: str, message: Optional[str] = None) -> None:
        msg = "Failed to import " + uri
        if message:
            msg = msg + ", " + message
        super().__init__(msg)

