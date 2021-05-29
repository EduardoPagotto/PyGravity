#!/usr/bin/env python3
'''
Created on 20200611
Update on 20210528
@author: Eduardo Pagotto
 '''

import array

from typing import Any, List, Tuple

import glm

from enum import Enum

EPSILON = 1e-2

class SIDE(Enum):
    CP_ONPLANE = 0
    CP_FRONT = 1
    CP_BACK = 2
    CP_SPANNING = 3

class Plane(object):
    def __init__(self):
        self.point: glm.vec3 = glm.vec3(0.0)
        self.normal: glm.vec3 = glm.vec3(0.0)
        self.ND: float = 0.0
        self.O: int = 0

    def set_values(self, a: glm.vec3, b: glm.vec3, c: glm.vec3):
        self.point = a
        self.normal = glm.normalize(glm.cross(b-a, c-a))

        self.ND = glm.dot(self.normal, a)


        cx1 = 0 if self.normal.x < 0.0 else 1 # down sw <----> se
        cx2 = 2 if self.normal.x < 0.0 else 3 # up   sw <----> se

        cx3 = 4 if self.normal.x < 0.0 else 5 # down nw <----> ne
        cx4 = 6 if self.normal.x < 0.0 else 7 # up   nw <----> ne

        cy1 = cx1 if self.normal.y < 0.0 else cx2 # down <----> up (sw-se)
        cy2 = cx3 if self.normal.y < 0.0 else cx4 # down <----> up (nw-ne)

        self.O = cy1 if self.normal.z < 0.0 else cy2 # back <----> front


    def collinearNormal(self, _normal: glm.vec3)->bool:
        sub: glm.vec3 = self.normal - _normal
        result: float = abs(sub.x + sub.y + sub.z)
        if result < EPSILON:
            return True

        return False


    def classifyPoint(self, point: glm.vec3)->SIDE:
        # ref: http://www.cs.utah.edu/~jsnider/SeniorProj/BSP/default.htm
        dir: glm.vec3 = self.point - point
        clipTest: float = glm.dot(dir, self.normal)

        if abs(clipTest) < EPSILON:
            return SIDE.CP_ONPLANE

        if clipTest < 0.0: # FIXME testar esta merda!!!!
            return SIDE.CP_FRONT

        return SIDE.CP_BACK

    def classifyPoly(self, pA: glm.vec3, pB: glm.vec3, pC: glm.vec3)->Tuple[SIDE, glm.vec3]:
        # ref: http://www.cs.utah.edu/~jsnider/SeniorProj/BSP/default.htm
        infront: int = 0
        behind: int = 0
        onPlane: int = 0
        result = array.array('f', [0.0, 0.0, 0.0])

        result[0] = glm.dot((self.point - pA), self.normal); # Clip Test poin A
        result[1] = glm.dot((self.point - pB), self.normal); # Clip Test poin B
        result[2] = glm.dot((self.point - pC), self.normal); # Clip Test poin C

        for a in range(3):
            if abs(result[a]) < EPSILON:
                result[a] = 0.0
                onPlane += 1
                infront += 1
                behind +=1
            elif result[a] > 0.0:
                behind += 1
            else:  # result[a] < 0.0
                infront += 1

        clipTest = glm.vec3(result[0], result[1], result[2])

        if onPlane == 3:
            return SIDE.CP_ONPLANE, clipTest

        if behind == 3:
            return SIDE.CP_BACK, clipTest

        if infront == 3:
            return SIDE.CP_FRONT, clipTest

        return SIDE.CP_SPANNING, clipTest


    def intersect(self, linestart: glm.vec3, lineend: glm.vec3)->Tuple[bool, glm.vec3, float]:

        direction: glm.vec3 = lineend - linestart

        linelength: float = glm.dot(direction, self.normal)

        if abs(linelength) < 0.0001:
            return False, glm.vec3(0.0), 0.0

        L1: glm.vec3  = self.point - linestart

        dist_from_plane: float = glm.dot(L1, self.normal)
        percentage: float = dist_from_plane / linelength

        if percentage < 0.0:
            return False, glm.vec3(0.0), percentage
        elif percentage > 1.0:
            return False, glm.vec3(0.0), percentage

        intersection: glm.vec3 = linestart + (direction * percentage)
        return True, intersection, percentage

    def AABB_Behind(self, AABBVertices: List[glm.vec3]) -> bool:
        val : float = glm.dot(self.normal, AABBVertices[self.O])
        val2 = val < self.ND
        return val2

    def AABB_Distance(self, AABBVertices: List[glm.vec3]) -> float:
        val = glm.dot(self.normal, AABBVertices[self.O])
        return val

