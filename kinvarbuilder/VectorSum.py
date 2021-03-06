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


from .kinvarbuilder import CachingFunction, IllegalArgumentTypes

from FourVector import FourVector
from TransverseVector import TransverseVector, Vector2D


@CachingFunction
class VectorSum:
    def __init__(self, inputObjects):

        # check that all input objects are either FourVector or TransverseVector objects

        if len(inputObjects) > 1:
            for vec in inputObjects:
                # for the moment we do not allow mixtures
                # of FourVector and TransverseVector,
                # just sums of FourVector
                # or a single TransverseVector
                if not isinstance(vec, FourVector):
                    raise IllegalArgumentTypes()

            self.allAreFourvectors = True
        else:
            # allow one single vector to be a TransverseVector

            if isinstance(inputObjects[0], FourVector):
                self.allAreFourvectors = True
            elif isinstance(inputObjects[0], TransverseVector):
                self.allAreFourvectors = False
            else:
                # other type, don't know how to use this for a vector sum
                raise IllegalArgumentTypes()

        # we can add FourVectors to FourVectors
        #
        # if we add a FourVector to a TransverseVector, we can only
        # get a TransverseVector out (the z components are ignored
        # in the end)

        self.inputObjects = list(inputObjects)

        if self.allAreFourvectors:
            # the vector to hold the sum
            import ROOT
            self.vector = ROOT.TLorentzVector()
        else:
            # a single TransverseVector
            self.vector = Vector2D()

    #----------------------------------------
    def getParents(self):
        # return the objects on which this one depends
        return self.inputObjects

    #----------------------------------------

    def isFourVector(self):
        # @return true if the sum is s fourvector quantity (i.e. all input vectors
        # are fourvectors) or false if the sum is a transverse vector
        #
        # for the moment, we just build sums of FourVectors
        # (while transverse vectors can be used as function arguments)

        return self.allAreFourvectors

    #----------------------------------------

    def numComponents(self):
        # returns the number of input vectors to this sum
        return len(self.inputObjects)

    #----------------------------------------

    def getValue(self):
        # @return the sum of vectors of the current event

        if self.allAreFourvectors:

            # sum the components by hand for the moment
            self.vector.SetXYZT(0,0,0,0)

            for obj in self.inputObjects:
                vector = obj.getValue()

                if vector == None:
                    # not defined for this event
                    return None

                self.vector += vector
        else:
            assert len(self.inputObjects) == 1

            vector = self.inputObjects[0].getValue()

            if vector == None:
                # not defined for this event
                return None
            
            # self.vector += vector
            self.vector = vector

        return self.vector

    #----------------------------------------

    def __str__(self):

        return " + ".join([str(x) for x in self.inputObjects])

    def __repr__(self):
        # not exactly what the __repr__ function should return
        # but helps in debugging
        return self.__str__()
