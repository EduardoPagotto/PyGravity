#!/usr/bin/env python3
'''
Created on 20210529
Update on 20210529
@author: Eduardo Pagotto
 '''

from typing import List

from PyGravity.render.Plane import Plane

import glm

from OpenGL.GL import * 

class Frustum(object):
    def __init__(self, ViewProjectionMatrixInverse: glm.mat4) -> None:
        super().__init__()

        self.vertices: List[glm.vec3] = []
        self.planes: List[Plane] = []
        for _ in range(6):
            self.planes.append(Plane())

        A: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4(-1.0, -1.0,  1.0, 1.0)
        B: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4( 1.0, -1.0,  1.0, 1.0)
        C: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4(-1.0,  1.0,  1.0, 1.0)
        D: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4( 1.0,  1.0,  1.0, 1.0)
        E: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4(-1.0, -1.0, -1.0, 1.0)
        F: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4( 1.0, -1.0, -1.0, 1.0)
        G: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4(-1.0,  1.0, -1.0, 1.0)
        H: glm.vec4 = ViewProjectionMatrixInverse * glm.vec4( 1.0,  1.0, -1.0, 1.0)

        self.vertices.append(glm.vec3(A.x / A.w, A.y / A.w, A.z / A.w))
        self.vertices.append(glm.vec3(B.x / B.w, B.y / B.w, B.z / B.w))
        self.vertices.append(glm.vec3(C.x / C.w, C.y / C.w, C.z / C.w))
        self.vertices.append(glm.vec3(D.x / D.w, D.y / D.w, D.z / D.w))
        self.vertices.append(glm.vec3(E.x / E.w, E.y / E.w, E.z / E.w))
        self.vertices.append(glm.vec3(F.x / F.w, F.y / F.w, F.z / F.w))
        self.vertices.append(glm.vec3(G.x / G.w, G.y / G.w, G.z / G.w))
        self.vertices.append(glm.vec3(H.x / H.w, H.y / H.w, H.z / H.w))

        self.planes[0].set_values(self.vertices[4], self.vertices[0], self.vertices[2])
        self.planes[1].set_values(self.vertices[1], self.vertices[5], self.vertices[7])
        self.planes[2].set_values(self.vertices[4], self.vertices[5], self.vertices[1])
        self.planes[3].set_values(self.vertices[2], self.vertices[3], self.vertices[7])
        self.planes[4].set_values(self.vertices[0], self.vertices[1], self.vertices[3])
        self.planes[5].set_values(self.vertices[5], self.vertices[4], self.vertices[6])


    def AABBVisible(self, AABBVertices: List[glm.vec3])->bool:
        for i in range(6):
            if self.planes[i].AABB_Behind(AABBVertices) is True:
                return False

        return True

    def AABBDistance(self, AABBVertices:List[glm.vec3]):
        return self.planes[5].AABB_Distance(AABBVertices) # 5 ????? FIXME: Que porra é esta ?????


    def render(self):
        glBegin(GL_LINES)

        glVertex3fv(glm.value_ptr(self.vertices[0]))
        glVertex3fv(glm.value_ptr(self.vertices[1]))
        glVertex3fv(glm.value_ptr(self.vertices[2]))
        glVertex3fv(glm.value_ptr(self.vertices[3]))
        glVertex3fv(glm.value_ptr(self.vertices[4]))
        glVertex3fv(glm.value_ptr(self.vertices[5]))
        glVertex3fv(glm.value_ptr(self.vertices[6]))
        glVertex3fv(glm.value_ptr(self.vertices[7]))

        glVertex3fv(glm.value_ptr(self.vertices[0]))
        glVertex3fv(glm.value_ptr(self.vertices[2]))
        glVertex3fv(glm.value_ptr(self.vertices[1]))
        glVertex3fv(glm.value_ptr(self.vertices[3]))
        glVertex3fv(glm.value_ptr(self.vertices[4]))
        glVertex3fv(glm.value_ptr(self.vertices[6]))
        glVertex3fv(glm.value_ptr(self.vertices[5]))
        glVertex3fv(glm.value_ptr(self.vertices[7]))

        glVertex3fv(glm.value_ptr(self.vertices[0]))
        glVertex3fv(glm.value_ptr(self.vertices[4]))
        glVertex3fv(glm.value_ptr(self.vertices[1]))
        glVertex3fv(glm.value_ptr(self.vertices[5]))
        glVertex3fv(glm.value_ptr(self.vertices[2]))
        glVertex3fv(glm.value_ptr(self.vertices[6]))
        glVertex3fv(glm.value_ptr(self.vertices[3]))
        glVertex3fv(glm.value_ptr(self.vertices[7]))

        glEnd()
