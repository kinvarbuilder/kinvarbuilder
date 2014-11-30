#!/usr/bin/env python

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

