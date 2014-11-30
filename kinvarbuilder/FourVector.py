#!/usr/bin/env python

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

        ### self.varPt = array.array('f',[ 0 ])
        ### self.varEta = array.array('f',[ 0 ])
        ### self.varPhi = array.array('f',[ 0 ])

        ### if isinstance(self.massName, float) or isinstance(self.massName, int):
        ###     # a fixed mass value has been set
        ###     self.varMass = array.array('f',[ self.massName ])
        ### else:
        ###     self.varMass = array.array('f',[ 0 ])

    #----------------------------------------

    def setTreeReader(self, treeReader):
        # TODO: we should watch out for overlaps of multiple fourvectors
        #       setting branches on the same variable

        # self.branchPt = tree.SetBranchAddress(self.ptName, self.)
        # tree.SetBranchAddress(self.ptName, self.varPt)
        # tree.SetBranchAddress(self.etaName, self.varEta)
        # tree.SetBranchAddress(self.phiName, self.varPhi)

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
