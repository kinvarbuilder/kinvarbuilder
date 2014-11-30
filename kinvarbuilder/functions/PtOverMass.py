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


from ..kinvarbuilder import CachingFunction

@CachingFunction
class PtOverMass:

    def __init__(self, vector1, vector2):

        self.vectors = [vector1, vector2]

        # we need fourvectors (even if massless, i.e. actually
        # more like a threevector) to calculate eta. Transverse
        # vectors won't work
        for vector in self.vectors:
            if not vector.isFourVector():
                raise IllegalArgumentTypes()

    def getValue(self):
        # TODO: for the moment we just calculate pt of the first vector (sum)
        # over the mass of both vectors combined. We should have a way
        # of specifying that the second vector should be taken

        mass = (self.vectors[0].getValue() + self.vectors[1].getValue()).M()

        return self.vectors[0].getValue().Pt() / mass

    @staticmethod
    def getNumArguments(maxNumArguments):
        return [ 2 ]