#!/usr/bin/env python3
'''
Created on 20200130
Update on 20200611
@author: Eduardo Pagotto
 '''

import glm

class AABB(object):
    def __init__(self, pos:glm.vec3, size:glm.vec3):
        self.pos = pos
        self.size = size
        self.max = self.pos + self.size
        self.min = self.pos - self.size
        self.surfaceArea = 2.0 * (self.size.x * self.size.y + self.size.x * self.size.z + self.size.y * self.size.z)

        self.vertex = [glm.vec3(self.min.x, self.min.y, self.min.z),
                       glm.vec3(self.max.x, self.min.y, self.min.z),
                       glm.vec3(self.min.x, self.max.y, self.min.z),
                       glm.vec3(self.max.x, self.max.y, self.min.z),
                       glm.vec3(self.min.x, self.min.y, self.max.z),
                       glm.vec3(self.max.x, self.min.y, self.max.z),
                       glm.vec3(self.min.x, self.max.y, self.max.z),
                       glm.vec3(self.max.x, self.max.y, self.max.z)]


    def _v3(self, val):
        return '({0:.2f} {1:.2f} {2:.2f})'.format(val.x, val.y, val.z)

    def __str__(self):
        return 'p:{0} s:{1}'.format(self._v3(self.pos), self._v3(self.size))

    def contains(self, point):
        return (point.x >= self.min.x and
                point.x < self.max.x and
                point.y >= self.min.y and
                point.y < self.max.y and
                point.z >= self.min.z and
                point.z < self.max.z)

    def intersects(self, other):
        return (other.min.x > self.max.x or
                other.max.x < self.min.x or
                other.min.y > self.max.y or
                other.max.y < self.min.y or
                other.min.z > self.max.z or
                other.max.z < self.min.z)

    def containsAABB(self, other):
        return (other.min.x >= self.min.x and
                other.max.x <= self.max.x and
                other.min.y >= self.min.y and
                other.max.y <= self.max.y and
                other.min.z >= self.min.z and
                other.max.z <= self.max.z)

    def overlapsAABB(self, other):
        return (self.max.x > other.min.x and
                self.min.x < other.max.x and
                self.max.y > other.min.y and
                self.min.y < other.max.y and
                self.max.z > other.min.z and
                self.min.z < other.max.z)

    # def merge(self, other):
    #     return AABB(glm.min(self.min, other.min), glm.max(self.max, other.max))

    # def intersection(self, other):
    #     return AABB(glm.min(self.max, other.max), glm.max(self.min, other.min))

    # def transformation(self, trans):
    #     # FIXME: esta errado!!!!
    #     self.min = glm.vec3(trans * glm.vec4(self.min, 1.0))
    #     self.max = glm.vec3(trans * glm.vec4(self.max, 1.0))

    # AABB AABB::transformation(const glm::mat4& transformation) {

    #     glm::vec3 val, min, max;
    #     for (short i = 0; i < 8; i++) {
    #         val = glm::vec3(transformation * glm::vec4(vertices[i], 1.0f));
    #         if (i != 0) {
    #             min = glm::min(min, val);
    #             max = glm::max(max, val);
    #         } else {
    #             min = val;
    #             max = val;
    #         }
    #     }