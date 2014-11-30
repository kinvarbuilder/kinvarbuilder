#!/usr/bin/env python

from ..kinvarbuilder import CachingFunction, IllegalArgumentTypes

@CachingFunction
class VectorDifferenceQuantity:
    # base class for quantities calculating a difference like
    # quantity of two (sums of) vectors

    #----------------------------------------

    def __init__(self, vector1, vector2, needFourvectors):
        # we actually take any kind of sum where we have
        # at least one vector of positive sign in the sum
        # and at least one vector with negative sign
        # (we sum those with the same sign first and
        # take the delta Eta between the sums of vectors
        # with different signs

        self.vectors = [vector1, vector2]

        if needFourvectors:
            # we need fourvectors (even if massless, i.e. actually
            # more like a threevector) to calculate eta. Transverse
            # vectors won't work
            for vector in self.vectors:
                if not vector.isFourVector():
                    raise IllegalArgumentTypes()


    @staticmethod
    def getNumArguments(maxNumArguments):
        return [ 2 ]
