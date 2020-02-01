#!/usr/bin/env python3
'''
Created on 20191114
Update on 20200201
@author: Eduardo Pagotto
 '''

import glm

from random import seed
from random import randint

#from PyGravity.render.AABB import AABB
from AABB import AABB

class Octree(object):
    def __init__(self, boundary, capacity, leafyMode=False, deep=0):
        self.boundary = boundary
        self.capacity = capacity
        self.leafyMode = leafyMode
        self.deep = deep
        self.points = []
        self.divided = False
        self.tnw = None
        self.tne = None
        self.tsw = None
        self.tse = None
        self.bnw = None
        self.bne = None
        self.bsw = None
        self.bse = None

    def __str__(self):
        return 'boundery:{0}'.format(self.boundary)

    def subdivide(self):

        p = self.boundary.pos
        s = self.boundary.size / 2
        new_deep = self.deep + 1
        self.divided = True

        xmax = p.x + s.x
        xmin = p.x - s.x
        ymax = p.y + s.y
        ymin = p.y - s.y
        zmax = p.z + s.z
        zmin = p.z - s.z

        tne = AABB(glm.vec3(xmax, ymax, zmax), s)
        tnw = AABB(glm.vec3(xmin, ymax, zmax), s)
        tsw = AABB(glm.vec3(xmin, ymax, zmin), s)
        tse = AABB(glm.vec3(xmax, ymax, zmin), s)
        
        bne = AABB(glm.vec3(xmax, ymin, zmax), s)
        bnw = AABB(glm.vec3(xmin, ymin, zmax), s)
        bsw = AABB(glm.vec3(xmin, ymin, zmin), s)
        bse = AABB(glm.vec3(xmax, ymin, zmin), s)

        self.tne = Octree(tne, self.capacity, self.leafyMode, new_deep)
        self.tnw = Octree(tnw, self.capacity, self.leafyMode, new_deep)
        self.tsw = Octree(tsw, self.capacity, self.leafyMode, new_deep)
        self.tse = Octree(tse, self.capacity, self.leafyMode, new_deep)

        self.bne = Octree(bne, self.capacity, self.leafyMode, new_deep)
        self.bnw = Octree(bnw, self.capacity, self.leafyMode, new_deep)
        self.bsw = Octree(bsw, self.capacity, self.leafyMode, new_deep)
        self.bse = Octree(bse, self.capacity, self.leafyMode, new_deep)

        
    def __insert_new(self, point):
        if self.tne.insert(point):
            return True

        if self.tnw.insert(point):
            return True

        if self.tse.insert(point):
            return True

        if self.tsw.insert(point):
            return True

        if self.bne.insert(point):
            return True

        if self.bnw.insert(point):
            return True

        if self.bse.insert(point):
            return True

        if self.bsw.insert(point):
            return True

    def insert(self, point):

        if self.boundary.contains(point) is not True:
            return False

        # by Karnaugh
        A = len(self.points) < self.capacity
        B = self.leafyMode is False
        C = self.divided is False

        if (A and B) or (A and C):
            self.points.append(point)
            return True
        else:
            if self.divided is False:
                self.subdivide()
                
            if self.leafyMode is True:
                for p in self.points:
                    self.__insert_new(p)
                    self.points = []
    
            self.__insert_new(point)

    def query(self, aabb, found):
        if not self.boundary.intersects(aabb):
            return
        else:
            for p in self.points:
                if aabb.contains(p):
                    found.append(p)
                
            if self.divided:
                self.tnw.query(aabb, found)
                self.tne.query(aabb, found)
                self.tsw.query(aabb, found)
                self.tse.query(aabb, found)
                self.bnw.query(aabb, found)
                self.bne.query(aabb, found)
                self.bsw.query(aabb, found)
                self.bse.query(aabb, found)
            
def randomic(boundary):
    randx = randint(boundary.min.x, boundary.max.x)
    randy = randint(boundary.min.y, boundary.max.y)
    randz = randint(boundary.min.z, boundary.max.z)

    return glm.vec3(randx, randy, randz)


if __name__ == '__main__':

    # seed(1)

    # boundary = AABB(pos=glm.vec3(200.0,200.0,200.0), size=glm.vec3(200.0,200.0,200.0))

    # oc = Octree(boundary, 4)
    # for _ in range(500):
    #     p = randomic(boundary)
    #     oc.insert(p)

    # #print(o.contains(glm.vec3(-6,10,10)))
    # print(str(oc))

    boundary = AABB(pos=glm.vec3(20.0, 20.0, 20.0), size=glm.vec3(20.0, 20.0, 20.0))

    oc = Octree(boundary, 1, True)

    for k in range(4):
        for j in range(4):
            for i in range(4):

                x = 5 + 10 * i
                y = 5 + 10 * j
                z = 5 + 10 * k

                oc.insert(glm.vec3(x,y,z))

    oc.insert(glm.vec2(7,18))

    print('fim')