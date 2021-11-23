#!/usr/bin/env python
# encoding: utf-8

import os
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    raise SystemExit("Python 3.8 or later is required.")

version = description = url = author = version_info = ''
exec(open(os.path.join("routines", "release.py")).read())

here = os.path.abspath(os.path.dirname(__file__))

trove_map = {
    'plan': "Development Status :: 1 - Planning",
    'alpha': "Development Status :: 3 - Alpha",
    'beta': "Development Status :: 4 - Beta",
    'final': "Development Status :: 5 - Production/Stable",
}

# Entry Point

setup(
    name = "routines",
    version = version,
    description = description,
    entry_points = {
        'protocol_client': [
        # https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml
        # https://www.w3.org/wiki/UriSchemes
            'ftp = routines.plugins:FTPInterface',
        ],
        'console_scripts': [
            'routines = routines.app:main',
        ],
        'uri.scheme': [
            'ftp-trace = uri.scheme:URLScheme',
        ],
    },
)
