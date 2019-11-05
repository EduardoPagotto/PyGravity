#!/usr/bin/env python3
'''
Created on 20160921
Update on 20191105
@author: Eduardo Pagotto
 '''

import math
from ctypes import *

# class POINTS(Structure):
#     _fields_ = [('x', c_double), 
#                 ('y', c_double), 
#                 ('z', c_double)] 

class Vec3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        '''Inicializa Vetor com 0.0 0.0 0.0'''
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str('{valx},{valy},{valz}'.format(valx = self.x, valy = self.y, valz = self.z))

    def __add__(self, other):
        '''Soma vetorial: v1 = v2 + v3'''
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x,y,z)

    def __sub__(self, other):
        '''Subitacao vetorial: v1 = v2 - v3'''
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x,y,z)

    def __mul__(self, escalar):
        '''Produto Vetorial, vetor multiplicado pelo escalar: v1 = v2 * real'''
        return Vec3(self.x * escalar,
            self.y * escalar,
            self.z * escalar)

    def __truediv__(self, escalar):
        '''Divisao de vetor por escalar v1 = v2 / real'''
        return Vec3(self.x / escalar,
                    self.y / escalar,
                    self.z / escalar)
    
    def __iadd__(self, other):
        '''Acumula vetor: v1 += v2'''
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return Vec3(self.x, self.y, self.z)

    def __isub__(self, other):
        '''Subrai acumulado v1 -= v2'''
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return Vec3(self.x, self.y, self.z)
        
    def distance(self, posicao):
        '''Distancia com a posicao'''
        return math.sqrt( math.pow( ( self.x - posicao.x ),2 ) + math.pow( ( self.y - posicao.y ),2 ) + math.pow( ( self.z - posicao.z ),2 ))
    
    def module(self):
        ''' Magnitude/comprimento do vetor '''
        amp = lambda vx, vy, vz :(vx ** 2 + vy **2 + vz ** 2) ** .5
        return amp(self.x, self.y, self.z)

    def versor(self):
        '''vetor com modulo tamanho igual a 1.0.'''
        modulo = self.module()
        return Vec3( self.x / modulo, self.y / modulo, self.z / modulo )

if __name__ == '__main__':
    
    vec1 = Vec3(2.0, 3.0, 4.0)
    vec2 = Vec3(5.0, 5.0, 5.0)

    vec2 -= vec1

    print('Vec:{0}'.format(vec2))
    val = vec2.module()
    print('Modulo:{0}'.format(val))
    #print('Versor:{0}'.format(vec2.versor())