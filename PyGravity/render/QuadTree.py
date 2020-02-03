#!/usr/bin/env python3
'''
Created on 20191109
Update on 20200201
@author: Eduardo Pagotto
 '''

import glm
from random import seed
from random import randint

#from PyGravity.render.Rectangle import Rectangle
from Rectangle import Rectangle

class QuadTree(object):
    def __init__(self, boundary, capacity, leafyMode=False, deep=0):
        self.boundary = boundary
        self.capacity = capacity
        self.leafyMode = leafyMode
        self.deep = deep
        self.points = []
        self.divided = False
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def __str__(self):
        return 'boundery:{0}'.format(self.boundary)

    def subdivide(self):

        p = self.boundary.pos
        s = self.boundary.size / 2
        new_deep = self.deep + 1
        self.divided = True

        # FIXME: considera a tela com 0,0 em top-left (opengl e botton-left)
        # para opengl trocar north com south
        ne = Rectangle(glm.vec2(p.x + s.x, p.y - s.y), s)
        nw = Rectangle(glm.vec2(p.x - s.x, p.y - s.y), s)
        se = Rectangle(glm.vec2(p.x + s.x, p.y + s.y), s)
        sw = Rectangle(glm.vec2(p.x - s.x, p.y + s.y), s)

        self.ne = QuadTree(ne, self.capacity, self.leafyMode, new_deep)
        self.nw = QuadTree(nw, self.capacity, self.leafyMode, new_deep)
        self.se = QuadTree(se, self.capacity, self.leafyMode, new_deep)
        self.sw = QuadTree(sw, self.capacity, self.leafyMode, new_deep)

    def __insert_new(self, point):
        if self.ne.insert(point):
            return True

        if self.nw.insert(point):
            return True

        if self.se.insert(point):
            return True

        if self.sw.insert(point):
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
    
        if self.divided is False:
            self.subdivide()
                
        if self.leafyMode is True:
            for p in self.points:
                self.__insert_new(p)

            self.points = []

        return self.__insert_new(point)

    def query(self, retangle, found):
        if not self.boundary.intersects(retangle):
            return
        
        for p in self.points:
            if retangle.contains(p):
                found.append(p)
            
        if self.divided:
            self.nw.query(retangle, found)
            self.ne.query(retangle, found)
            self.sw.query(retangle, found)
            self.se.query(retangle, found)
            
def randomic(boundary):
    randx = randint(boundary.pos.x - boundary.size.x, boundary.pos.x + boundary.size.x)
    randy = randint(boundary.pos.x - boundary.size.x, boundary.pos.y + boundary.size.y)
    return glm.vec2(randx, randy)

if __name__ == '__main__':
    # seed(1)
    # boundary = Rectangle(glm.vec2(200, 200), glm.vec2(200, 200))
    # qt = QuadTree(boundary, 1, True)
    # for _ in range(150):
    #     qt.insert(randomic(boundary))
    # print(str(qt))

    boundary = Rectangle(glm.vec2(20,20), glm.vec2(20,20))

    qt = QuadTree(boundary, 1, True)

    for i in range(4):
        for j in range(4):
            x = 5 + 10 * i
            y = 5 + 10 * j

            qt.insert(glm.vec2(x,y))

    qt.insert(glm.vec2(7,18))

    print('fim')
