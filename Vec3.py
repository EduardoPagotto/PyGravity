##!#/usr/bin/python3.5
'''
Created on 21 de set de 2016

@author: pagotto
'''
import math
from ctypes import *

class POINTS(Structure):
    _fields_ = [('x', c_double), 
                ('y', c_double), 
                ('z', c_double)] 

class Vec3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str('{valx},{valy},{valz}'.format(valx = self.x, valy = self.y, valz = self.z))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x,y,z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x,y,z)

    def __mul__(self, escalar):
        return Vec3(self.x * escalar,
            self.y * escalar,
            self.z * escalar)

    def __truediv__(self, escalar):
        return Vec3(self.x / escalar,
                    self.y / escalar,
                    self.z / escalar)

    def divisor(self, escalar):
        return Vec3(self.x / escalar,
                    self.y / escalar,
                    self.z / escalar)


    def distance(self, posicao):
        return math.sqrt( math.pow( ( self.x - posicao.x ),2 ) + math.pow( ( self.y - posicao.y ),2 ) + math.pow( ( self.z - posicao.z ),2 ))

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    # def prod(self, escalar):
    #      return Vec3(self.x * escalar,
    #                     self.y * escalar,
    #                     self.z * escalar)
    
    def amplitude(self):
        amp = lambda vx, vy, vz :(vx ** 2 + vy **2 + vz ** 2) ** .5
        return amp(self.x, self.y, self.z)

if __name__ == '__main__':
    
    vec = Vec3(3.0, 4.0, 5.0)
    print('Vec:{0}'.format(vec))
    val = vec.amplitude()
    print('Amplitude:{0}'.format(val))
