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


from .kinvarbuilder import CachingFunction

@CachingFunction
class FourVector:
    """ threevectors can be modeled by setting the mass to 0 """

    #----------------------------------------

    def __init__(self, pt, eta, phi, mass = 0, name = None):

        # pt, eta, phi must contain names of variables in a ROOT TTree
        self.ptName  = pt
        self.etaName = eta
        self.phiName = phi
        self.massName = mass

        if name == None:
            if self.ptName.lower().endswith('pt'):
                name = self.ptName[:-2]
            else:
                name = self.ptName
        
        self.name = name

        # raise Exception("implement creation of variables to read values from tree")

        # the vector to hold the values
        import ROOT
        self.vector = ROOT.TLorentzVector()

        # if self.massName == None, this is a three vector
        # and we assume the mass is zero all the time
        # TODO: support a fixed mass value (e.g. for tau leptons or b jets)


    #----------------------------------------

    def setTreeReader(self, treeReader):
        # TODO: we should watch out for overlaps of multiple fourvectors
        #       setting branches on the same variable

        self.varPt = treeReader.getVar(self.ptName)
        self.varEta = treeReader.getVar(self.etaName)
        self.varPhi = treeReader.getVar(self.phiName)

        if isinstance(self.massName, float) or isinstance(self.massName, int):
            # a fixed mass value has been set
            self.varMass = [ self.massName ]
        else:
            self.varMass = treeReader.getVar(self.massName)


    #----------------------------------------


    def getValue(self):
        # get the quantities from the tree
        self.vector.SetPtEtaPhiM(
                self.varPt[0],
                self.varEta[0],
                self.varPhi[0],
                self.varMass[0])
        return self.vector

    #----------------------------------------

    def __str__(self):
        return self.name

    def __repr__(self):
        # not exactly what the __repr__ function should return
        # but helps in debugging
        return self.__str__()