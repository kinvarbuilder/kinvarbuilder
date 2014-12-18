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


from ..kinvarbuilder import CachingFunction, IllegalArgumentTypes
import math

@CachingFunction
class TransverseMass:

    #----------------------------------------
    def __init__(self, vector1, vector2):

        self.vector1 = vector1
        self.vector2 = vector2
    
    #----------------------------------------
    def getParents(self):
        return [ self.vector1, self. vector2 ]

    #----------------------------------------

    def getValue(self):

        vecVal1 = self.vector1.getValue()
        vecVal2 = self.vector2.getValue()

        if vecVal1 == None or vecVal2 == None:
            return None

        # calculate the transverse mass

        et = vecVal1.Et() + vecVal2.Et()

        px = vecVal1.Px() + vecVal2.Px()
        py = vecVal1.Py() + vecVal2.Py()

        diff = et * et - px * px - py * py

        if diff >= 0:
            return math.sqrt(diff)
        else:
            return - math.sqrt(- diff)
    
    #----------------------------------------

    @staticmethod
    def getNumArguments(maxNumArguments):
        # for the moment, require exactly two arguments
        if maxNumArguments >= 2:
            return [ 2 ]
        else:
            return [   ]

    #----------------------------------------

    def __str__(self):
        return "MT(" + str(self.vector1) + "," + str(self.vector2) + ")"

    #----------------------------------------
