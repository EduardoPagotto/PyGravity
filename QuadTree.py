#!/usr/bin/env python3
'''
Created on 20191109
Update on 20191114
@author: Eduardo Pagotto
 '''

import glm
from random import seed
from random import randint

class Rectangle(object):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.max = pos + size
        self.min = pos - size
        
    def __str__(self):
        return 'pos:{0}, y:{1}, w:{2}, h:{3}'.format(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def contains(self, point):
        return (point.x >= self.min.x and
                point.x < self.max.x and
                point.y >= self.min.y and
                point.y < self.max.y)

    def intersects(self, retangle):
        return not (retangle.min.x > self.max.x or
                    retangle.max.x < self.min.x or
                    retangle.min.y > self.max.y or
                    retangle.max.y < self.min.y)
    
class QuadTree(object):
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None
        self.divided = False

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

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)

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
                
            if self.northeast.insert(point):
                return True

            if self.northwest.insert(point):
                return True

            if self.southeast.insert(point):
                return True

            if self.southwest.insert(point):
                return True
        

    def query(self, retangle, found):
        if not found:
            found = []
        
        if not self.boundary.intersects(retangle):
            return
        else:
            for p in self.points:
                if retangle.contains(p):
                    found.push(p)
                
            if self.divided:
                self.northwest.query(retangle, found)
                self.northeast.query(retangle, found)
                self.southwest.query(retangle, found)
                self.southeast.query(retangle, found)
            
        return found
    
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

    
