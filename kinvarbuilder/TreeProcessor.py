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

        #----------
        # create an output tree with the variables
        #----------

        if outputFileName != None:
            import ROOT
            fout = ROOT.TFile(outputFileName, "RECREATE")
        else:
            fout = None

        outTree = ROOT.TNtuple(outputTreeName,"output tree",
                               ":".join(self.varBuilder.outputVarnames))

        import array
        outputValues =  array.array("f", [ 0.0 ] * len(self.varBuilder.outputVarnames))

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

            # TODO: add support for quantity not existing
            # for i in range(len(values)):
            #    if values[i] == None:
            #        values[i] = -999.0

            # print ",".join(str(x) for x in outputValues)

            # fill the output tree
            outTree.Fill(outputValues)

        # write the output tree to the file
        if fout != None:
            fout.cd()
            outTree.Write()

            # TODO: go back to the ROOT directory we were before instead of going to ROOT.gROOT

            ROOT.gROOT.cd()
            fout.Close()
