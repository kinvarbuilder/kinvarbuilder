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


from .TreeReader import TreeReader

class TreeProcessor:
    """ reads an input tree and produces the additional output variables.
        Can be called multiple times after instantiation
    """

    #----------------------------------------

    def __init__(self, varBuilder):

        self.varBuilder = varBuilder

        self.spectatorExpressions = []
        self.spectatorOutputVariableNames = []

    #----------------------------------------

    def addSpectatorVariable(self, expression, outputName = None):
        """
        adds a ROOT expression to be also put into the output tree, e.g. for checking
        or distinguishing signal from background or event weights etc.

        :param expression:
        """

        if outputName == None:
            outputName = expression


        # TODO: check that there are no duplicate output variable names
        self.spectatorExpressions.append(expression)
        self.spectatorOutputVariableNames.append(outputName)

    #----------------------------------------

    def makeTree(self, inputTree, outputTreeName, outputFileName = None, maxEvents = None,
                 # firstEvent = None,
                 progressCallback = None):
        """
        produce a ROOT output tree

        :param inputTree: the tree from which the variables shall be calculated
        :param outputTreeName: must be specified: the name of the output tree produced
        :param outputFileName: optional: if given, a TFile is created and the generated tree is written
            to this file
        :param maxEvents: process at most this number of events (unless it is None)
        :param firstEvent: the number of the first event to process
        :param progressCallback: a function taking the pointer to this class and the index (0 based) of
         the event about to be processed
        :return:
        """

        treeReader = TreeReader(inputTree)

        # set the input tree
        # (note that for the moment this is not thread safe)
        for vector in self.varBuilder.inputVectors:
            vector.setTreeReader(treeReader)

        # add spectator expressions to the treeReader
        spectatorBuffers = [ treeReader.getVar(expression) for expression in self.spectatorExpressions ]

        #----------
        # create an output tree with the variables
        #----------

        if outputFileName != None:
            import ROOT
            fout = ROOT.TFile(outputFileName, "RECREATE")
        else:
            fout = None

        allOutputVarNames = self.varBuilder.outputVarnames + self.spectatorOutputVariableNames

        outTree = ROOT.TNtuple(outputTreeName,"output tree",
                               ":".join(allOutputVarNames))

        import array
        # buffer for TTree.Fill(..)
        outputValues =  array.array("f", [ 0.0 ] * len(allOutputVarNames))

        #----------
        # loop over all lines of the data given
        #----------

        for eventIndex in range(treeReader.numEvents):

            if maxEvents != None and eventIndex >= maxEvents:
                break

            if progressCallback != None:
                progressCallback(maxEvents, eventIndex)

            # read the event into memory
            treeReader.getEvent(eventIndex)

            # clear the caches from the previous event
            for obj in self.varBuilder.outputScalars:
                obj.newEvent()

            # calculate the derived quantities
            for index, derivedQuantity in enumerate(self.varBuilder.outputScalars):
                outputValues[index] = derivedQuantity.getValue()

            # copy the values for additional expressions to be put into the tree
            for index, buffer in enumerate(spectatorBuffers):
                outputValues[len(self.varBuilder.outputScalars) + index] = buffer[0]

            # TODO: add support for quantity not existing
             # fill the output tree
            outTree.Fill(outputValues)

        # write the output tree to the file
        if fout != None:
            fout.cd()
            outTree.Write()

            # TODO: go back to the ROOT directory we were before instead of going to ROOT.gROOT

            ROOT.gROOT.cd()
            fout.Close()

    #----------------------------------------    

    def makeArray(self, inputTree, maxEvents = None,
                  firstEvent = 0,
                  progressCallback = None):
        """
        :return: a numpy record array with the values of the new variables
        :param: firstEvent is the index of the first event to process (zero based)
        """

        treeReader = TreeReader(inputTree)

        #----------
        # determine the number of rows in the array to return
        #----------
        if maxEvents != None:
            endEvent = min(firstEvent + maxEvents, treeReader.numEvents)
        else:
            endEvent = treeReader.numEvents            

        numEventsToProcess = endEvent - firstEvent

        #----------
        # create a record array
        #----------
        # see e.g. http://docs.scipy.org/doc/numpy/user/basics.rec.html

        import numpy

        # TODO: do we have to create an array of zeros or can we create
        #       an uninitialized array ?

        dtypes = [ (varname, 'f4') for varname in self.varBuilder.outputVarnames ]

        retval = numpy.zeros(numEventsToProcess, dtype = dtypes)

        #----------
        # set the input tree
        #----------

        # (note that for the moment this is not thread safe)
        for vector in self.varBuilder.inputVectors:
            vector.setTreeReader(treeReader)


        #----------
        # loop over all lines of the data given
        #----------

        # row into the returned matrix
        rowIndex = 0

        for eventIndex in range(firstEvent, endEvent):


            if maxEvents != None and eventIndex >= maxEvents:
                break

            if progressCallback != None:
                progressCallback(maxEvents, eventIndex)

            # read the event into memory
            treeReader.getEvent(eventIndex)

            # clear the caches from the previous event
            for obj in self.varBuilder.outputScalars:
                obj.newEvent()

            # calculate the derived quantities
            for index, derivedQuantity in enumerate(self.varBuilder.outputScalars):
                retval[rowIndex][index] = derivedQuantity.getValue()

            # TODO: add support for quantity not existing

            # prepare next iteration
            rowIndex += 1

        # end of loop over all events in range

        return retval

    #----------------------------------------    
