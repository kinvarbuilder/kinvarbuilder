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

#----------------------------------------------------------------------

import sys

def maxCumulativeDifference(valuesSig, valuesBkg, weightsSig, weightsBkg):
    # from scipy.stats import ks_2samp

    # there seems NOT to be a Kolmogorov-Smirnov test for weighted
    # samples in python but since all variables have the same
    # number of values, we just can compare the difference in the cumulative
    # distribution for the moment

    # calculate the weighted cumulative distributions

    # sortedValuesSig, sortedSumWeightsSig = cumulativeSum(valuesSig, weightsSig)
    # sortedValuesBkg, sortedSumWeightsBkg = cumulativeSum(valuesBkg, weightsBkg)

    sumWeightsSig = sum(weightsSig)
    sumWeightsBkg = sum(weightsBkg)

    numEventsSig = len(valuesSig)
    numEventsBkg = len(valuesBkg)

    # see also scipy.ks_2samp(..)
    # make a combined list of all data points
    #
    # since we also have to keep track of the weights, we work with indices
    # note that both samples need not to have the same number of entries,
    # so we work with a scheme where the indices are:
    #   0 .. numEventsSig - 1                           : signal events
    #   numEventsSig .. numEventsSig + numEventsBkg - 1 : background events

    def isSignal(index):
        return index < numEventsSig

    def getValue(index):
        if index < numEventsSig:
            return valuesSig[index]
        else:
            return valuesBkg[index - numEventsSig]

    def getWeight(index):
        if index < numEventsSig:
            return weightsSig[index]
        else:
            return weightsBkg[index - numEventsSig]

    indices = range(numEventsSig + numEventsBkg)

    # sort signal and background together by increasing value
    indices.sort(key = getValue)

    cumulativeSumSoFar = 0

    maxDiff = 0

    for index in indices:
        weight = getWeight(index)
        if isSignal(index):
            cumulativeSumSoFar += weight / sumWeightsSig
        else:
            cumulativeSumSoFar -= weight / sumWeightsBkg

        # update the maximum difference
        maxDiff = max(maxDiff, abs(cumulativeSumSoFar))


    return maxDiff


#----------------------------------------------------------------------

class VariableRanking:

    #----------------------------------------

    def __init__(self, valuesSig, valuesBkg, weightColSig = None, weightColBkg = None, columnsToCompare = None,
                 varDescriptions = None):
        """
        :param valuesSig: a numpy record array for the signal events
        :param valuesBkg: same as valuesSignal but for background
        :param columnsToCompare: if not None, restrict the comparison to the given columns
        :param variableDescriptions: if not None, specifies a mapping of output variable names to the string
            to be printed instead
        """

        #----------
        # get the event weights
        #----------

        if weightColSig == None:
            # assume all weights are one
            weightsSig = numpy.ones(len(valuesSig))
        else:
            weightsSig = valuesSig[weightColSig]

        if weightColBkg == None:
            # assume all weights are one
            weightsBkg = numpy.ones(len(valuesBkg))
        else:
            weightsBkg = valuesBkg[weightColBkg]

        #----------
        # find the variables to be compared
        #----------
        if columnsToCompare == None:
            # take all columns (except the weight columns),
            # insist that both signal and background have
            # the same columns
            columnsToCompare = self.__getColumNames(valuesSig, weightColSig)
            if set(columnsToCompare) != set(self.__getColumNames(valuesBkg, weightColBkg )):
                raise Exception("signal and background seem to have different variables")


        #----------
        # compare the variables
        #----------

        self.columns = columnsToCompare

        self.similarities = []

        self.varDescriptions = []

        for colname in columnsToCompare:
            self.similarities.append(self.calcSimilarity(valuesSig[colname], valuesBkg[colname], weightsSig, weightsBkg))

            varDescription = colname
            if varDescriptions != None:
                varDescription = varDescriptions.get(colname, colname)

            self.varDescriptions.append(varDescription)


    #----------------------------------------

    def __getColumNames(self, values, weightColName):
        retval = list(values.dtype.names)

        if weightColName != None:
            try:
                retval.remove(weightColName)
            except ValueError:
                pass

        return retval

    #----------------------------------------

    def calcSimilarity(self, valuesSig, valuesBkg, weightsSig, weightsBkg):
        return maxCumulativeDifference(valuesSig, valuesBkg, weightsSig, weightsBkg)


    #----------------------------------------

    def printSummary(self, os = sys.stdout):
        print >> os,"similarity ranking (least similar variables first):"

        indices = range(len(self.similarities))

        # reverse = True will make put the most dissimilar variable first
        indices.sort(key = lambda i: self.similarities[i], reverse = True)

        maxWidth = max(len(name) for name in self.varDescriptions)

        for index in indices:
            print >> os,"  %-*s : %f" % (maxWidth, self.varDescriptions[index], self.similarities[index])


#----------------------------------------------------------------------
