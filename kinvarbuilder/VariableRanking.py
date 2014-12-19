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

import sys, os

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

    # when we have lots of events with the same value,
    # the sorting could be such that we first have
    # all the background and then all the signal
    # events which would look like that there is discrimination
    # power in this region but there is not because
    # we could not put a cut between signal and background
    # (because the events have the same values here)

    lastValue = None

    for index in indices:
        weight = getWeight(index)

        value = getValue(index)

        assert lastValue == None or value >= lastValue

        if isSignal(index):
            cumulativeSumSoFar += weight / sumWeightsSig
        else:
            cumulativeSumSoFar -= weight / sumWeightsBkg

        # update the maximum difference
        # only update this if the value of the variable
        # actually increased (see the discussion above)
        if value > lastValue:
            maxDiff = max(maxDiff, abs(cumulativeSumSoFar))

        # prepare the next iteration
        lastValue = value


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
            self.weightsSig = numpy.ones(len(valuesSig))
        else:
            self.weightsSig = valuesSig[weightColSig]

        if weightColBkg == None:
            # assume all weights are one
            self.weightsBkg = numpy.ones(len(valuesBkg))
        else:
            self.weightsBkg = valuesBkg[weightColBkg]

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

        self.valuesSig = []
        self.valuesBkg = []
        

        for colname in columnsToCompare:
            self.similarities.append(self.calcSimilarity(valuesSig[colname], valuesBkg[colname], self.weightsSig, self.weightsBkg))

            # keep the signal and background values for generating a report later
            self.valuesSig.append(valuesSig[colname])
            self.valuesBkg.append(valuesBkg[colname])

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

    #----------------------------------------

    def plotVariableToImageFile(self, varIndex, foutName):

        # determine the binning: take 50 bins from min to max
        # (add some margin on the left and right)
        values = list(self.valuesSig[varIndex]) + list(self.valuesBkg[varIndex])
        xmin = min(values)
        xmax = max(values)

        numbins = 50
        numbinsWithMargin = numbins + 2

        binWidth = (xmax - xmin) / float(numbins)

        # add some margin
        xmid = 0.5 * (xmin + xmax)
        
        xmin = xmid - (numbinsWithMargin * binWidth) / 2.0
        xmax = xmid + (numbinsWithMargin * binWidth) / 2.0

        import ROOT

        histoSig = ROOT.TH1F("",self.varDescriptions[varIndex],numbinsWithMargin, xmin, xmax)
        histoBkg = ROOT.TH1F("",self.varDescriptions[varIndex],numbinsWithMargin, xmin, xmax)

        histoSig.SetLineColor(ROOT.kRed)
        histoBkg.SetLineColor(ROOT.kBlue)

        histoSig.SetLineWidth(2)
        histoBkg.SetLineWidth(2)

        for values, weights, histo in (
            (self.valuesSig[varIndex], self.weightsSig, histoSig),
            (self.valuesBkg[varIndex], self.weightsBkg, histoBkg),
            ):
            for i in range(len(values)):
                histo.Fill(values[i], weights[i])

        # normalize histograms to unit are
        for histo in (histoSig, histoBkg):
            tot = histo.GetSum()
            if tot > 0:
                histo.Scale(1 / float(tot))

        ymax = max(histoSig.GetMaximum(), histoBkg.GetMaximum()) * 1.1

        histoSig.SetMaximum(ymax)
        histoBkg.SetMaximum(ymax)

        # TODO: can we prevent ROOT from drawing an actual window on the screen
        canv = ROOT.TCanvas()

        histoSig.Draw()
        histoBkg.Draw("same")

        canv.SaveAs(foutName)

        canv.Close()
        

    #----------------------------------------

    def writeHtmlReport(self,fout):
        # sort by decreasing smilarity
        indices = range(len(self.similarities))

        # reverse = True will make put the most dissimilar variable first
        indices.sort(key = lambda i: self.similarities[i], reverse = True)

        # fout must be a file like object

        print >> fout,"<html>"
        print >> fout,"<head>"
        print >> fout,"<title>variable ranking</title>"
        print >> fout,"</head>"

        print >> fout,"<body>"

        print >> fout, "<h1>variable ranking</h1>"

        #----------
        # print an overview table
        #----------
        print >> fout, "<table>"
        print >> fout, "<tr><th>dissimilarity rank</th><th>expression</th><th>dissimilarity</th></tr>"

        for index,varIndex in enumerate(indices):

            items = [ index + 1,
                      ('<a href="#%d">' % (index + 1)) + self.varDescriptions[varIndex] + "</a>",
                      self.similarities[varIndex],
                      ]

            print >> fout, "<tr>", "".join([ "<td>" + str(x) + "</td>" for x in items ]),"</tr>"
        

        print >> fout, "</table>"


        #----------

        import tempfile
        workdir = tempfile.mkdtemp()

        for index,varIndex in enumerate(indices):

            varDescription = self.varDescriptions[varIndex]

            print >> fout, "<hr/>"

            # HTML anchor
            print >> fout, '<a name="%d"/>' % (index + 1)

            print >> fout, "<h2>" + varDescription + "</h2>"

            print >> fout, "dissimilarity rank:",index + 1,"<br/>"
            print >> fout, "dissimilarity:",self.similarities[varIndex],"<br/>"

            fname = os.path.join(workdir, "%d.png" % varIndex)
            self.plotVariableToImageFile(varIndex, fname)

            # read the png file back
            fin = open(fname)
            imageData = fin.read()
            fin.close()

            os.unlink(fname)

            # put the image as data URI directly into the html
            import base64
            print >> fout,'<img src="data:image/png;base64,%s" />' % base64.b64encode(imageData)
            


        # end of loop over all variables


        print >> fout,"</body>"
        print >> fout,"</html>"
        
        

        


#----------------------------------------------------------------------
