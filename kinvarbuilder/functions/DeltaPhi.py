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

import math

class DeltaPhi(VectorDifferenceQuantity):
    """angle in transverse plane between vectors """


    def __init__(self, vector1, vector2):

        # no requirement on the input vectors to be
        # fourvectors
        VectorDifferenceQuantity.__init__(self, vector1, vector2, False)

    def getValue(self):

        vecValues = [ vec.getValue() for vec in self.vectors ]

        for vecVal in vecValues:
            if vecVal == None:
                return None


        phi1 = vecValues[0].Phi()
        phi2 = vecValues[1].Phi()

        diff = phi1 - phi2

        while diff > math.pi:
            diff -= 2 * math.pi

        while diff <= - math.pi:
            diff += 2 * math.pi

        return diff

    def __str__(self):
        return "DeltaPhi(" + ", ".join(str(v) for v in self.vectors) +")"