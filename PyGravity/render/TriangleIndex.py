#!/usr/bin/env python3
'''
Created on 20210529
Update on 20210529
@author: Eduardo Pagotto
 '''

import array

import glm

class TriangleIndex(object):
    def __init__(self) -> None:
        self.beenUsedAsSplitter:bool = False
        self.p = array.array('L', [0,0,0]) # PA = 0; PB = 1; PC = 2
        self.normal: glm.vec3 = glm.vect3(0.0)

    def deepCopy(self, origem:'TriangleIndex')->None:
        self.beenUsedAsSplitter = origem.beenUsedAsSplitter
        self.normal = origem.normal
        self.p[0] = origem.p[0]
        self.p[1] = origem.p[1]
        self.p[2] = origem.p[2]