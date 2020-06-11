#!/usr/bin/env python3
'''
Created on 20200611
Update on 20200611
@author: Eduardo Pagotto
 '''

import glm

class Plane(object):
    def __init__(self):
        self.point = None
        self.normal = None
        self.ND = 0.0
        self.O = 0

    def set_values(self, a:glm.vec3, b:glm.vec3, c:glm.vec3):
        self.point = a
        self.normal = glm.normalize(glm.cross(b-a, c-a))

        self.ND = glm.dot(self.normal, a)

        cx1 = 0 if self.normal.x < 0.0 else 1 # down sw <----> se
        cx2 = 2 if self.normal.x < 0.0 else 3 # up   sw <----> se

        cx3 = 4 if self.normal.x < 0.0 else 5 # down nw <----> ne
        cx4 = 6 if self.normal.x < 0.0 else 7 # up   nw <----> ne

        cy1 = cx1 if self.normal.y < 0.0 else cx2 # down <----> up (sw-se)
        cy2 = cx3 if self.normal.y < 0.0 else cx4 # down <----> up (nw-ne)

        self.O = cy1 if self.normal.z < 0.0 else cy2

    def AABB_Behind(self, AABBVertices):
        val = glm.dot(self.normal, AABBVertices[self.O])
        val2 = val < self.ND
        return val2

    def AABB_Distance(self, AABBVertices):
        val = glm.dot(self.normal, AABBVertices[self.O])
        return val

