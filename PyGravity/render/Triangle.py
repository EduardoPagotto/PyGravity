#!/usr/bin/env python3
'''
Created on 20200210
Update on 20200611
@author: Eduardo Pagotto
 '''

import glm
from PyGravity.core.VertexData import VertexData

class Triangle(object):
    def __init__(self, a : glm.vec3, b : glm.vec3, c : glm.vec3):
        self.vertex = []

        va = VertexData()
        va.position = a
        va.normal = glm.vec3(0.0)
        va.texture = glm.vec2(0.0)
        self.vertex.append(va)

        vb = VertexData()
        vb.position = b
        vb.normal = glm.vec3(0.0)
        vb.texture = glm.vec2(0.0)
        self.vertex.append(vb)

        vc = VertexData()
        vc.position = c
        vc.normal = glm.vec3(0.0)
        vc.texture = glm.vec2(0.0)
        self.vertex.append(vc)

    def deepyCopy(self, t):
        self.vertex[0] = t.vertex[0]
        self.vertex[1] = t.vertex[1]
        self.vertex[2] = t.vertex[2]


    def normal(self) -> glm.vec3:
        acc = glm.vec3(0, 0, 0)

        for i in range(3):
            acc = acc + self.vertex[i].normal

        return glm.vec3(acc.x / 3, acc.y / 3, acc.z / 3)

