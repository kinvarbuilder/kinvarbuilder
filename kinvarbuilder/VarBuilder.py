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


from .functions import *

from .kinvarbuilder import makePartitions, IllegalArgumentTypes
from VectorSum import VectorSum

class VarBuilder:
    """ creates the new variables given a list of fourvectors
    """

    #----------------------------------------

    def __init__(self, inputVectors, initialStateZcomponentKnown):
        # @param initialStateZcomponentKnown is typically set to true for lepton
        # colliders and false for hadron colliders

        self.inputVectors = inputVectors
        self.initialStateZcomponentKnown = initialStateZcomponentKnown

        self.listOfFunctions = []

        # compile the list of functions to be applied
        self.listOfFunctions.extend(
            [
            Mass,        # should NOT be used on single vectors ?
            ### funcPt,      # should NOT be used on single vectors ?

            DeltaPhi,

            PtOverMass,

            ]
        )

        if self.initialStateZcomponentKnown:
            #----------
            # lepton collider type quantities
            #----------

            self.listOfFunctions.extend([
                Angle3D,
            ])

        else:
            #----------
            # hadron collider type quantities
            #----------

            self.listOfFunctions.extend([
                AbsDeltaEta,
                ### AbsEta,

                # DEBUG
                Angle3D,


            ])

    #----------------------------------------

    def makeDerived(self):
        # can also be called after the list of functions was customized by the caller

        # TODO: should we support things like sum of scalars (e.g. sums of pts) ?

        self.outputScalars = []

        # maps from the number of subgroups to the list of partitions of this size
        nSizedPartitions = {}

        # for vectorCombination in allVectorCombinations:

        for func in self.listOfFunctions:

            # see how many vector (sums) this function wants
            numArgumentsList = func.getNumArguments(len(self.inputVectors))

            for numArguments in numArgumentsList:

                if not nSizedPartitions.has_key(numArguments):
                    # create all possible partitions with numArguments groups
                    # and create sums of these
                    groups = makePartitions(self.inputVectors, numArguments)

                    for line in groups:
                        print line

                    # produce vector sums of these
                    sums = [
                        [ VectorSum(group) for group in line ]
                        for line in groups
                    ]

                    nSizedPartitions[numArguments] = sums
                else:
                    sums = nSizedPartitions[numArguments]

                # create a function for these

                for line in sums:

                    try:
                        self.outputScalars.append(func(*line))
                    except IllegalArgumentTypes:
                        # this function can not be applied to the given set of vectors
                        pass

            # end of loop over possible number of arguments of the current function

        # end of loop over functions to apply to the vector combinations

        self.outputVarnames = [ "out%02d" % index for index in range(len(self.outputScalars))]