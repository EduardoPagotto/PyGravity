#!/usr/bin/env python3
'''
Created on 20200130
Update on 20200714
@author: Eduardo Pagotto
 '''

import glm

class Rectangle(object):
    def __init__(self, pos:glm.vec2, size:glm.vec2):
        self.pos = pos
        self.size = size
        self.max = pos + size
        self.min = pos - size

    def __str__(self) -> str:
        return 'pos:{0}, y:{1}, w:{2}, h:{3}'.format(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def contains(self, point) -> bool:
        return (point.x >= self.min.x and
                point.x < self.max.x and
                point.y >= self.min.y and
                point.y < self.max.y)

    def intersects(self, retangle) -> bool:
        return not (retangle.min.x > self.max.x or
                    retangle.max.x < self.min.x or
                    retangle.min.y > self.max.y or
                    retangle.max.y < self.min.y)
