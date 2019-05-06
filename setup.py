#!/usr/bin/python -u
#
# Python Bindings for libevent
#
# Copyright (c) 2010-2011 by Joachim Bauch, mail@joachim-bauch.de
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import shutil
from setuptools import setup, find_packages
from distutils.command.build import build as _build

shutil.copy('patches/buildfix__init__.py', 'libevent/__init__.py')

class _PatchesBuildCommand(_build):
    def __init__(self, *args, **kwargs):
        _build.__init__(self, *args, **kwargs)
    
    def run(self):
        shutil.copy('patches/__init__.py', 'libevent/__init__.py')
        return _build.run(self)

import sys, os

try:
    from setuptools import setup, Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

    from setuptools import setup, Extension

import libevent.version

LIBEVENT_ROOT = os.environ.get('LIBEVENT_ROOT')
if LIBEVENT_ROOT is None:
    raise TypeError('Please set the environment variable LIBEVENT_ROOT ' \
        'to the path of your libevent root directory and make sure ' \
        'to pass "--with-pic" to configure when building it')

descr = "Python bindings for libevent"
modules = [
    'libevent/libevent',
]
c_files = [
    'libevent/src/_libevent.c',
    'libevent/src/pybase.c',
    'libevent/src/pybuffer.c',
    'libevent/src/pybufferevent.c',
    'libevent/src/pyevent.c',
    'libevent/src/pyhttp.c',
    'libevent/src/pylistener.c',
]
include_dirs = [
    os.path.join(LIBEVENT_ROOT, 'include'),
]
library_dirs = [
]
libraries = [
]
extra_link_args = [
]
if os.name == 'posix':
    # enable thread support
    extra_link_args.extend([
        os.path.join(LIBEVENT_ROOT, '.libs', 'libevent.a'),
        os.path.join(LIBEVENT_ROOT, '.libs', 'libevent_pthreads.a'),
    ])
    libraries.append('rt')
    libraries.append('pthread')
elif os.name == 'nt':
    # enable thread support
    extra_link_args.extend([
        os.path.join(LIBEVENT_ROOT,  'libevent.lib'),
    ])    
    libraries.append('ws2_32')
    libraries.append('Advapi32')
    
extens = [
    Extension('libevent/_libevent', c_files, libraries=libraries,
        include_dirs=include_dirs, library_dirs=library_dirs,
        extra_link_args=extra_link_args),
]

setup(
    name = 'syncwerk-server-python-libevent',
    version = '20190423',
    author = 'Syncwerk GmbH',
    author_email = 'support@syncwerk.com',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url = 'https://www.syncwerk.com',
    license = 'LGPL',
    description = 'Python Libevent',
    long_description='Python bindings for libevent',
    py_modules = modules,
    ext_modules = extens,
    test_suite = 'tests.suite',
    include_package_data=True,
    cmdclass={"build": _PatchesBuildCommand}
)
