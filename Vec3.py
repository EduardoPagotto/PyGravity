'''
Created on 21 de set de 2016

@author: pagotto
'''
import math

class Vec3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str('{valx},{valy},{valz}'.format(valx = self.x, valy = self.y, valz = self.z))  

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

    def prod(self, escalar):
         return Vec3(self.x * escalar,
                        self.y * escalar,
                        self.z * escalar)

if __name__ == '__main__':
    
    vec = Vec3()
    print('Vec:{0}'.format(vec))

