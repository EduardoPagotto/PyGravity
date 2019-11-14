#!/usr/bin/env python3
'''
Created on 20191114
Update on 20191114
@author: Eduardo Pagotto
 '''

import glm

from random import seed
from random import randint

class Octant(object):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.max = self.pos + self.size
        self.min = self.pos - self.size

    def __str__(self):
        return 'pos:{0} size:{1}'.format(self.pos, self.size)

    def contains(self, point):
        return (point.x >= self.min.x and
                point.x < self.max.x and
                point.y >= self.min.y and
                point.y < self.max.y and
                point.z >= self.min.z and
                point.z < self.max.z)
                 
    def intersects(self, range):
        return (range.pos.x - range.size.x > self.max.x or
                range.pos.x + range.size.x < self.min.x or
                range.pos.y - range.size.y > self.max.y or
                range.pos.y + range.size.y < self.min.y or
                range.pos.z - range.size.z > self.max.z or
                range.pos.z + range.size.z < self.min.z)


class Octree(object):
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []

        self.top_northwest = None
        self.top_northeast = None
        self.top_southwest = None
        self.top_southeast = None

        self.botton_northwest = None
        self.botton_northeast = None
        self.botton_southwest = None
        self.botton_southeast = None

        self.divided = False

    def __str__(self):
        return 'boundery:{0}'.format(self.boundary)


    def subdivide(self):

        p = self.boundary.pos
        s = self.boundary.size / 2

        xmax = p.x + s.x
        xmin = p.x - s.x
        ymax = p.y + s.y
        ymin = p.y - s.y
        zmax = p.z + s.z
        zmin = p.z - s.z

        tne = Octant(glm.vec3(xmax, ymax, zmax), s)
        tnw = Octant(glm.vec3(xmin, ymax, zmax), s)
        tsw = Octant(glm.vec3(xmin, ymax, zmin), s)
        tse = Octant(glm.vec3(xmax, ymax, zmin), s)
        
        bne = Octant(glm.vec3(xmax, ymin, zmax), s)
        bnw = Octant(glm.vec3(xmin, ymin, zmax), s)
        bsw = Octant(glm.vec3(xmin, ymin, zmin), s)
        bse = Octant(glm.vec3(xmax, ymin, zmin), s)

        self.top_northeast = Octree(tne, self.capacity)
        self.top_northwest = Octree(tnw, self.capacity)
        self.top_southwest = Octree(tsw, self.capacity)
        self.top_southeast = Octree(tse, self.capacity)

        self.botton_northeast = Octree(bne, self.capacity)
        self.botton_northwest = Octree(bnw, self.capacity)
        self.botton_southwest = Octree(bsw, self.capacity)
        self.botton_southeast = Octree(bse, self.capacity)

        self.divided = True


    def insert(self, point):

        if self.boundary.contains(point) is not True:
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if self.divided is False:
                self.subdivide()
                
            if self.top_northeast.insert(point):
                return True

            if self.top_northwest.insert(point):
                return True

            if self.top_southeast.insert(point):
                return True

            if self.top_southwest.insert(point):
                return True

            if self.botton_northeast.insert(point):
                return True

            if self.botton_northwest.insert(point):
                return True

            if self.botton_southeast.insert(point):
                return True

            if self.botton_southwest.insert(point):
                return True


def randomic(boundary):
    randx = randint(boundary.min.x, boundary.max.x)
    randy = randint(boundary.min.y, boundary.max.y)
    randz = randint(boundary.min.z, boundary.max.z)

    return glm.vec3(randx, randy, randz)


if __name__ == '__main__':

    seed(1)

    boundary = Octant(pos=glm.vec3(200.0,200.0,200.0), size=glm.vec3(200.0,200.0,200.0))

    oc = Octree(boundary, 4)


    for _ in range(500):
        p = randomic(boundary)
        oc.insert(p)

    #print(o.contains(glm.vec3(-6,10,10)))
    print(str(oc))