#!/usr/bin/env python
#
# kinvarbuilder - A library for searching kinematic variables in a systematic way
#
# Copyright 2014 University of California, San Diego
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(
    name = 'kinvarbuilder',
    version = '0.0',
    url = 'https://github.com/kinvarbuilder/kinvarbuilder/',
    license = 'Apache Software License Version 2.0',
    author = 'Andre Holzner',
    tests_require = [],
    install_requires = [],
    author_email = 'andre.holzner@gmail.com',
    description = 'A library for building kinematic variables systematically',
    long_description = '',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        ],
    extras_require = { }
)

