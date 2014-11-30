#!/usr/bin/env python

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


import os
import glob

# import all functions in the current directory

# get all .py files in this directory
pythonFiles = glob.glob(os.path.dirname(__file__)+"/*.py")

__all__ = []

# getattr(__import__('Mass', fromlist=['.Mass']),'Mass')

funcNames = [ os.path.basename(pythonFile)[:-3] for pythonFile in pythonFiles ]

for funcName in funcNames:
    if funcName == '__init__':
        continue

    # getattr(__import__(funcName, fromlist=["." + funcName]), funcName)
    __all__.append(funcName)

    # __import__(funcName, locals(), globals())

    # locals()[funcName] = getattr(locals()[funcName],funcName)

    locals()[funcName] = getattr(__import__(funcName, locals(), globals()), funcName)

#----------
# cleanup
#----------
del funcName
del funcNames
del pythonFiles
del pythonFile

del os
del glob