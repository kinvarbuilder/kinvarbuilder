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

class AbsDeltaEta(VectorDifferenceQuantity):
    """ delta Eta for indistinguishable particles """

    # TODO: can we somehow add information to a FourVector
    #       to check whether two particles are indistinguishable
    #       or not ?

    def __init__(self, vector1, vector2):
        VectorDifferenceQuantity.__init__(self, vector1, vector2, True)

    def getValue(self):
        return abs(self.vectors[0].getValue().Eta() - self.vectors[1].getValue().Eta())

    def __str__(self):
        return "AbsDeltaEta(" + ", ".join(str(v) for v in self.vectors) +")"