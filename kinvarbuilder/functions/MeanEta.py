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


from .VectorDifferenceQuantity import VectorDifferenceQuantity
from ..kinvarbuilder import CachingFunction, IllegalArgumentTypes

@CachingFunction
class MeanEta(VectorDifferenceQuantity):
    """ average pseudorapidity of two or more vectors, as a generalization
    of the mean pseudorapidity proposed by Zeppenfeld et. al. in hep-ph/9605444"""

    def __init__(self, *vectors):
        self.vectors = vectors

        for vector in self.vectors:
            if not vector.isFourVector():
                raise IllegalArgumentTypes()

    def getValue(self):
        vecValues = [ vec.getValue() for vec in self.vectors ]

        for vecVal in vecValues:
            if vecVal == None:
                return None

        sumEta = sum([ vec.Eta() for vec in vecValues ])
        return sumEta / float(len(vecValues))

    @staticmethod
    def getNumArguments(maxNumArguments):
        return range(2, maxNumArguments + 1)

    #----------------------------------------
    def getParents(self):
        return self.vectors

    #----------------------------------------
    def __str__(self):
        return "MeanEta(" + ",".join([ str(x) for x in self.vectors]) + ")"

    #----------------------------------------
