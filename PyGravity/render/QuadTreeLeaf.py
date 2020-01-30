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

class QuadTreeLeafy(object):
    def __init__(self, boundary):
        self.boundary = boundary
        self.point = None
        self.divided = False

        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None


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

        self.northeast = QuadTreeLeafy(ne)
        self.northwest = QuadTreeLeafy(nw)
        self.southeast = QuadTreeLeafy(se)
        self.southwest = QuadTreeLeafy(sw)

        self.divided = True

    def __insert_new(self, point):
        if self.northeast.insert(point):
            return True

        if self.northwest.insert(point):
            return True

        if self.southeast.insert(point):
            return True

        if self.southwest.insert(point):
            return True

    def insert(self, point):

        if self.boundary.contains(point) is not True:
            return False

        if (self.point is None) and (self.divided is False):
            self.point = point
            return True
        else:
            if self.divided is False:
                self.subdivide()

            if self.point is not None:
                self.__insert_new(self.point)
                self.point = None

            return self.__insert_new(point)

    def query(self, retangle, found):        
        if not self.boundary.intersects(retangle):
            return
        else:
            if self.point is not None:
                if retangle.contains(self.point):
                    found.append(self.point)
                
            if self.divided:
                self.northwest.query(retangle, found)
                self.northeast.query(retangle, found)
                self.southwest.query(retangle, found)
                self.southeast.query(retangle, found)
            
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

    qt = QuadTreeLeafy(boundary)

    for i in range(4):
        for j in range(4):
            x = 5 + 10 * i
            y = 5 + 10 * j

            qt.insert(glm.vec2(x,y))

    qt.insert(glm.vec2(7,18))
    found = []
    qt.query(Rectangle(glm.vec2(20,20), glm.vec2(20,20)), found)

    print('Localizados: %s',str(found))

    print('fim')

    
