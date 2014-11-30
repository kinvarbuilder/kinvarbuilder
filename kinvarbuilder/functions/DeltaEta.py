#!/usr/bin/env python

from .VectorDifferenceQuantity import VectorDifferenceQuantity

class DeltaEta(VectorDifferenceQuantity):
    """ delta pseudorapidity between two vectors """

    def __init__(self, vector1, vector2):
        VectorDifferenceQuantity.__init__(self, vector1, vector2, True)

    def getValue(self):
        return self.vectors[0].getValue().Eta() - self.vectors[1].getValue().Eta()
