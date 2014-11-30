#!/usr/bin/env python

from .kinvarbuilder import CachingFunction, IllegalArgumentTypes

from FourVector import FourVector


@CachingFunction
class VectorSum:
    def __init__(self, inputObjects):

        # check that all input objects are either FourVector or TransverseVector objects

        self.allAreFourvectors = True
        for vec in inputObjects:
            if isinstance(vec, FourVector):
                continue

            if isinstance(vec, TransverseVector):
                self.allAreFourvectors = False
                continue

            # other type, don't know how to use this for a vector sum
            raise IllegalArgumentTypes()

        # we can add FourVectors to FourVectors
        #
        # if we add a FourVector to a TransverseVector, we can only
        # get a TransverseVector out

        self.inputObjects = list(inputObjects)

        # the vector to hold the sum
        import ROOT
        self.vector = ROOT.TLorentzVector()


    #----------------------------------------
    def getParents(self):
        # return the objects on which this one depends
        return self.inputObjects

    #----------------------------------------

    def isFourVector(self):
        # @return true if the sum is s fourvector quantity (i.e. all input vectors
        # are fourvectors) or false if the sum is a transverse vector

        return self.allAreFourvectors

    #----------------------------------------

    def numComponents(self):
        # returns the number of input vectors to this sum
        return len(self.inputObjects)

    #----------------------------------------

    def getValue(self):
        # @return the sum of vectors of the current event

        # sum the components by hand for the moment
        self.vector.SetXYZT(0,0,0,0)

        for obj in self.inputObjects:
            vector = obj.getValue()
            self.vector += vector

        return self.vector

    #----------------------------------------

    def __str__(self):

        return " + ".join([str(x) for x in self.inputObjects])

    def __repr__(self):
        # not exactly what the __repr__ function should return
        # but helps in debugging
        return self.__str__()

