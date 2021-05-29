#!/usr/bin/env python3
'''
Created on 20200211
Update on 20200611
@author: Eduardo Pagotto
 '''

import glm

from PyGravity.render.AABB import AABB
from PyGravity.render.Plane import Plane

# class Tris(object):
#     def __init__(self, a:glm.vec3, b:glm.vec3, c:glm.vec3):
#         self.vertex = [a, b, c]
#         self.normal = glm.normalize(glm.cross(b-a, c-a))

if __name__ == "__main__":

    aabb = AABB(glm.vec3(0.0, 0.0, 0.0), glm.vec3(10.0, 10.0, 10.0))

    Va = glm.vec3(5.0, -20.0, 5.0)
    Vb = glm.vec3(5.0, -20.0, -5.0)
    Vc = glm.vec3(-5.0, -20.0, -5.0)

    plane = Plane()
    plane.set_values(Va, Vb, Vc)


    atras = plane.AABB_Behind(aabb.vertex)
    distancia = plane.AABB_Distance(aabb.vertex)

    print('Contem:{0}, Distancia:{1}'.format(atras, distancia))




