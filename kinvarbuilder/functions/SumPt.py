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
class SumPt:
    """ scalar sum of transverse momenta of two or more objects
    (which themselves can be sums of vectors)
    """
    # TODO: this function is invariant under the permutations
    #       of the parameters, i.e. we might produce the same
    #       quantity multiple times

    def __init__(self, *args):

        self.vectors = args

    def getValue(self):
        # TODO: for the moment we just calculate pt of the first vector (sum)
        # over the mass of both vectors combined. We should have a way
        # of specifying that the second vector should be taken

        return sum(vector.getValue().Pt() for vector in self.vectors)

    def getParents(self):
        return self.vectors

    @staticmethod
    def getNumArguments(maxNumArguments):
        # for the moment, we exclude the pt of a single
        # vector assuming that this is tested elsewhere

        return range(2, maxNumArguments + 1)

