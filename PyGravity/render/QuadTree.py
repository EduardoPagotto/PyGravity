#!/usr/bin/env python3
'''
Created on 20191109
Update on 20200130
@author: Eduardo Pagotto
 '''

import glm
from random import seed
from random import randint

#from PyGravity.render.Rectangle import Rectangle
from Rectangle import Rectangle

class QuadTree(object):
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
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
        
        # FIXME: considera a tela com 0,0 em top-left (opengl e botton-left)
        # para opengl trocar north com south
        ne = Rectangle(glm.vec2(p.x + s.x, p.y - s.y), s)
        nw = Rectangle(glm.vec2(p.x - s.x, p.y - s.y), s)
        se = Rectangle(glm.vec2(p.x + s.x, p.y + s.y), s)
        sw = Rectangle(glm.vec2(p.x - s.x, p.y + s.y), s)

        self.ne = QuadTree(ne, self.capacity)
        self.nw = QuadTree(nw, self.capacity)
        self.se = QuadTree(se, self.capacity)
        self.sw = QuadTree(sw, self.capacity)

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
                
            if self.ne.insert(point):
                return True

            if self.nw.insert(point):
                return True

            if self.se.insert(point):
                return True

            if self.sw.insert(point):
                return True
        

    def query(self, retangle, found):
        if not self.boundary.intersects(retangle):
            return
        else:
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

    # qt = QuadTree(boundary, 4)

    # for _ in range(50):
    #     qt.insert(randomic(boundary))

    # print(str(qt))

    boundary = Rectangle(glm.vec2(20,20), glm.vec2(20,20))

    qt = QuadTree(boundary, 1)

    for i in range(4):
        for j in range(4):
            x = 5 + 10 * i
            y = 5 + 10 * j

            qt.insert(glm.vec2(x,y))

    print('fim')

    
