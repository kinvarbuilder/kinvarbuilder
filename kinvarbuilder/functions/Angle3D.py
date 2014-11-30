#!/usr/bin/env python

from .VectorDifferenceQuantity import VectorDifferenceQuantity

class Angle3D(VectorDifferenceQuantity):
    """3D angle between vectors

     At a hadron collider (where at least one of the particles
     colliding is a particle with substructure), this typically does not
     make sense since we don't know the z component
     of the initial state and thus physics must
     be invariant under boosts along the beam pipe

     """

    def __init__(self, vector1, vector2):
        VectorDifferenceQuantity.__init__(self, vector1, vector2, True)

    def getValue(self):

        return self.vectors[0].getValue().Angle(self.vectors[1].getValue().Vect())
