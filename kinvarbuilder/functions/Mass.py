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

@CachingFunction
class Mass:

    #----------------------------------------
    def __init__(self, vectorSum):

        # do NOT take masses of single vectors
        # (although for jets this could make sense ?)
        
        if vectorSum.numComponents() < 2:
            raise IllegalArgumentTypes()

        self.vectorSum = vectorSum
    
    #----------------------------------------
    def getParents(self):
        return [ self.vectorSum ]

    #----------------------------------------

    def getValue(self):
        vecVal = self.vectorSum.getValue()

        if vecVal == None:
            return None
        return vecVal.M()
    
    #----------------------------------------

    @staticmethod
    def getNumArguments(maxNumArguments):
        # needs one group of vectors
        # to calculate the sum
        return [ 1 ]

    #----------------------------------------

    def __str__(self):
        return "Mass(" + str(self.vectorSum) +")"

    #----------------------------------------
