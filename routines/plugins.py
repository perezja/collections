import os
import sys
import ftplib
import logging
import random
import time

from abc import ABC, abstractmethod
from typing import Callable, List, Tuple, Mapping	
from common import Records
from pkg_resources import iter_entry_points

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout) 
formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)  

class ProtocolInterface(ABC):
    """Abstraction of client connection to the resource server""" 
    def __init__(self, host: str=None):
        self.host = host
        self.failed_attempts = 0
        self.max_attempts = 5
        self.welcome=None

        self.stop_when_connected()

    @abstractmethod
    def _connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _list(self, path: str) -> Records:
        raise NotImplementedError()

    def connect(self):
        logger.info("CONNECT {} ATTEMPT".format(self.host))
        self._connect()
        logger.info("CONNECT {} SUCCESS".format(self.host))
        if self.welcome:
            logger.info("{}".format(self.welcome))

    def ls(self, path) -> Records:
        return self._list(path)

    def stop_when_connected(self) -> None:
        try:
            self.connect()
        except ftplib.all_errors:
            logger.warning("CONNECT FAILED: {}; trying again...".format(self.host))
            time.sleep(5 * random.uniform(0.5, 1.5))
            self.stop_when_connected()

    @classmethod
    def __subclasshook__(cls, subcls):
        return (hasattr(subcls, '_list') and 
                callable(subcls._list) and 
                hasattr(subcls, '_connect') and 
                callable(subcls._connect) or 
                NotImplemented)

class FTPInterface(ProtocolInterface):

    def __init__(self, host:str, parser='mlsd'):
        super().__init__(host)
       
        if parser is None:
            # try to guess on first access
            logger.info("No parser provided; will guess on first attempt.")
            self._listfn = None

        elif callable(parser):
            # supply a custom listing parser
            logger.info("Supplied a custom dir listing parser.")
            self._listfn = parser
        elif parser == 'mlsd':
            logger.info("Set parser to MLSD.")
            self._listfn = self._list_mlsd
        elif parser == 'unix':
            logger.info("Set parser to UNIX.")
            self._listfn = self._list_unix
        elif parser == 'windows':
            logger.info("Set parser to WINDOWS.")
            self._listfn = self._list_windows
    
    def _connect(self):
        # attempt an anonymous FTP connection
        self.ftp = ftplib.FTP(self.host, user='anonymous', timeout=60)
        self.welcome = self.ftp.getwelcome()
        self.ftp.login()

    def _list(self, path):
        # public fn to get a path listing
        # guesses the format if it's not explicitly set
        try:
            if not self._listfn:
                self._listfn = self._guess_parser(path)

            records = self._listfn(path)
            self.failed_attempts = 0
            return records
        except:
            self.failed_attempts += 1
            self.ftp.close()
            logger.warning("LIST FAILED {}; Failed {} times out of {}; reconnecting...".format(path, self.failed_attempts, self.max_attempts))
            time.sleep(2 * random.uniform(0.5, 1.5))
            self.stop_when_connected()

   
    def _guess_parser(self, path):
        # also check out this library: http://cr.yp.to/ftpparse.html
        logger.info("Guessing FTP listing parser for {}...".format(self.host))
        try:
            lines = []
            self.ftp.retrlines("MLSD {}".format(path), lines.append)
            logger.info("Guessing parser: MLSD success")
            return self._list_mlsd
        
        except:
            logger.info("Guessing parser: MLSD fail")
        
        # not MLSD, so:
        # get a listing and check a few properties
        dir_in_3rd = lambda line: "<DIR>" in line.split()[2]
        numeric_first_letter = lambda line: line[0] >= '0' and line[0] <= '9'
        unix_first_letter = lambda line: line[0] in 'd-lpsbc'
        
        lines = []
        self.ftp.retrlines('LIST {}'.format(path, lines.append))
        
        # check for windows
        if (any(map(dir_in_3rd, lines)) and
                all(map(numeric_first_letter, lines))):
            logger.info("Guessing parser: WINDOWS")
            return self._list_windows
        
        # check for unix
        if all(map(unix_first_letter, lines)):
            logger.info("Guessing parser: UNIX")
            return self._list_unix
        
        logger.error('\n'.join(lines))
        raise RuntimeError("Failed to guess parser.")
    
    # these functions interact with the FTP with no error checking
    # they just take a path and try to return properly-formatted data
    def _list_mlsd(self, path):
        # copy of MLSD impl from Python 3.3 ftplib package that returns
        # listing data in a machine-readable format
        cmd = 'MLSD %s' % path
        lines = []
        self.ftp.retrlines(cmd, lines.append)
        results = []
        for line in lines:
            facts_found, _, name = line.rstrip('\r\n').partition(' ')
            entry = {}
            for fact in facts_found[:-1].split(";"):
                key, _, value = fact.partition("=")
                entry[key.lower()] = value
            results.append((name, entry))
        return results
    
    def _list_windows(self, path):
        lines = []
        self.ftp.dir(path, lines.append)
        results = []
        for line in lines:
            fields = line.split()
            name = ' '.join(fields[3:])
            size = -1
            if fields[2].strip() == '<DIR>':
                type_ = 'dir'
            else:
                type_ = 'file'
                size = int(fields[2])
            results.append((name, {'type': type_, 'size': size}))
        return results
    
    def _list_unix(self, path):
        lines = []
        self.ftp.dir(path, lines.append)
        results = []
        for line in lines:
            fields = line.split()
            name = ' '.join(fields[8:])
            size = -1
            if line[0] == 'd':
                type_ = 'dir'
            elif line[0] == '-':
                type_ = 'file'
                size = int(fields[4])
            elif line[0] == 'l':
                continue
            else:
                raise ValueError("Don't know what kind of file I have: %s" % line.strip())
            results.append((name, {'type': type_, 'size': size}))
        return results

def get_schemes(scheme):
    # obtains the uri.scheme entry point from package `uri` whcih maps schemes 
    # to uri.scheme.URLScheme objects
    pl, = iter_entry_points('uri.scheme', scheme)
    sch = pl.load()
    return(sch)

def get_plugin(scheme: str) -> Callable:
    try: 
        pl, = iter_entry_points('protocol_client', scheme)
        pcl = pl.load() 
        return(pcl)

    except Exception as e:
        logger.error(e)

class Impl:
    def _connect(self):
        pass
    def _list(self, path):
        pass

class NotImpl:
    def _connect(self):
        pass


