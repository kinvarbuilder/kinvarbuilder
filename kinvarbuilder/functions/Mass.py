#!/usr/bin/env python

from ..kinvarbuilder import CachingFunction, IllegalArgumentTypes

@CachingFunction
class Mass:

    #----------------------------------------
    def __init__(self, vectorSum):

        # do NOT take masses of single vectors
        # (although for jets this could make sense ?)
        
        if vectorSum.numComponents() < 2:
            raise IllegalArgumentTypes()

        self.vectorSum = vectorSum
    
    #----------------------------------------
    def getParents(self):
        return [ self.vectorSum ]

    #----------------------------------------

    def getValue(self):
        return self.vectorSum.getValue().M()
    
    #----------------------------------------

    @staticmethod
    def getNumArguments(maxNumArguments):
        # needs one group of vectors
        # to calculate the sum
        return [ 1 ]

    #----------------------------------------
