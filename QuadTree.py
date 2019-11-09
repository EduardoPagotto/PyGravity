#!/usr/bin/env python3
'''
Created on 20191109
Update on 20191109
@author: Eduardo Pagotto
 '''

#import glm
from random import seed
from random import randint

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '({0} {1})'.format(self.x, self.y)

class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return 'x:{0}, y:{1}, w:{2}, h:{3}'.format(self.x, self.y, self.w, self.h)

    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x < self.x + self.w and
                point.y >= self.y - self.h and
                point.y < self.y + self.h)

    def intersects(self, range):
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)
    


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

        x = self.boundary.x
        y = self.boundary.y

        size_w = self.boundary.w / 2
        size_h = self.boundary.h / 2
        
        # FIXME: considera a tela com 0,0 em top-left (opengl e botton-left)
        # para opengl trocar north com south
        ne = Rectangle(x + size_w, y - size_h, size_w, size_h)
        nw = Rectangle(x - size_w, y - size_h, size_w, size_h)
        se = Rectangle(x + size_w, y + size_h, size_w, size_h)
        sw = Rectangle(x - size_w, y + size_h, size_w, size_h)

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
        

    def query(self, range, found):
        if not found:
            found = []
        
        if not self.boundary.intersects(range):
            return
        else:
            for p in self.points:
                if range.contains(p):
                    found.push(p)
                
            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southwest.query(range, found)
                self.southeast.query(range, found)
            
        return found
    
def randomic(boundary):
    randx = randint(0, boundary.x + boundary.w)
    randy = randint(0, boundary.y + boundary.h)

    return Point(randx, randy)

if __name__ == '__main__':
    
    seed(1)
    boundary = Rectangle(200, 200, 200, 200)

    qt = QuadTree(boundary, 4)

    for _ in range(50):
        qt.insert(randomic(boundary))

    print(str(qt))
