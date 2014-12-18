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


# TODO: review in which cases it makes sense to convert a fourvector
#       back to a transverse vector to add it to a transverse vector
#

from .kinvarbuilder import CachingFunction
import math

# our own implementation of a transverse vector
# (which can have mass). ROOT's TVector2 seems
# not to know any mass method
class Vector2D:

    def __init__(self):
        self.px = 0
        self.py = 0
        self.e = 0
        

    def SetPhiEtPt(self, phi, et, pt):
        if pt == None:
            # assume a massless vector
            pt = et

        self.px = pt * math.cos(phi)
        self.py = pt * math.sin(phi)

        self.e = et
        
    def M(self):

        diff = self.e * self.e - self.px * self.px - self.py * self.py

        if diff >= 0:
            return math.sqrt(diff)
        else:
            return - math.sqrt(- diff)

    def Px(self):
        return self.px

    def Py(self):
        return self.py

    def Et(self):
        return self.e

    def Phi(self):
        return math.atan2(self.py, self.px)
        

    def Pt(self):
        return math.sqrt(self.px * self.px + self.py * self.py)

@CachingFunction
class TransverseVector:
    """ a transverse vector (typically at a hadron collider), i.e. the component
    parallel to the beam pipe is not known.

    """

    #----------------------------------------

    def __init__(self, phi, et, pt = None, name = None, validExpr = None):
        """

        :param pt: the missing transverse momentum. If None, then
           this object is assumed to be massless.
           
        :param validExpr: if not None, this is a ROOT tree expression which
          indicates if this vector is valid for a given event (nonzero value)
          or not (zero value)
        :return:
        """

        # pt, eta, phi must contain names of variables in a ROOT TTree
        self.etName  = et
        self.phiName = phi

        if pt == None:
            # will give a massless vector
            self.ptName = et
        else:
            self.ptName = pt

        if name == None:
            if self.etName.lower().endswith('et'):
                name = self.etName[:-2]
            else:
                name = self.etName
        
        self.name = name

        # the vector to hold the values
        import ROOT
        self.vector = Vector2D()

        self.validExpr = validExpr

    #----------------------------------------

    def setTreeReader(self, treeReader):
        self.varEt = treeReader.getVar(self.etName)
        self.varPt = treeReader.getVar(self.ptName)
        self.varPhi = treeReader.getVar(self.phiName)

        if self.validExpr != None:
            self.varValidExpr = treeReader.getVar(self.validExpr)
        else:
            self.varValidExpr = [ True ]

    #----------------------------------------


    def getValue(self):

        if not self.varValidExpr[0]:
            # this vector is not defined for the current event
            return None

        # get the quantities from the tree
        self.vector.SetPhiEtPt(
                self.varPhi[0],
                self.varEt[0],
                self.varPt[0],
            )
        return self.vector

    #----------------------------------------

    def __str__(self):
        return self.name

    def __repr__(self):
        # not exactly what the __repr__ function should return
        # but helps in debugging
        return self.__str__()
