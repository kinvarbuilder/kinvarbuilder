#!/usr/bin/env python

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
