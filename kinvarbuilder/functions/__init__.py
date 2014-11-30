#!/usr/bin/env python

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
