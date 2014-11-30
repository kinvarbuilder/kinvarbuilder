#!/usr/bin/env python

from .VectorDifferenceQuantity import VectorDifferenceQuantity

import math

class DeltaPhi(VectorDifferenceQuantity):
    """angle in transverse plane between vectors """


    def __init__(self, vector1, vector2):

        # no requirement on the input vectors to be
        # fourvectors
        VectorDifferenceQuantity.__init__(self, vector1, vector2, False)

    def getValue(self):

        phi1 = self.vectors[0].getValue().Phi()
        phi2 = self.vectors[1].getValue().Phi()

        diff = phi1 - phi2

        while diff > math.pi:
            diff -= 2 * math.pi

        while diff <= - math.pi:
            diff += 2 * math.pi

        return diff
