# encoding: utf-8
# type: ignore

"""Release information for the routines package."""

from collections import namedtuple

level_map = {'plan': '.dev'}

version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial')) \
		(0, 0, 0, 'plan', 0)

version = ".".join([str(i) for i in version_info[:3]]) + \
		((level_map.get(version_info.releaselevel, version_info.releaselevel[0]) + \
		str(version_info.serial)) if version_info.releaselevel != 'final' else '')  

author = namedtuple('Author', ['name', 'email'])("James A. Perez", 'perezja@wustl.edu')

description = "Index a DAG into metadata collections for parallelization of workflow execution"
url = 'https://github.com/perezja/routines/'
