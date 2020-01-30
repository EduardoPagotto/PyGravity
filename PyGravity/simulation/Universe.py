#!/usr/bin/env python3
'''
Created on 20160921
Update on 20200130
@author: Eduardo Pagotto
 '''

import glm
from PyGravity.simulation.Body import Body

class Universe(object):
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.listBody = []

    def __str__(self):
        return str('Tamanho:{0} Corpos:{1}' .format(self.tamanho, len(self.listBody)))

    def isInside(self, posicao):
        distancia = glm.length(posicao) # TODO: verificar
        if distancia <= self.tamanho:
            return True

        return False

if __name__ == '__main__':
    universo = Universe(100.0)

    universo.listBody.append( Body('c1', 100.0, glm.vec3(10.0, 10.0, 10.0)))
    universo.listBody.append( Body('c2', 100.0, glm.vec3(20.0, 10.0, -10.0)))
    universo.listBody.append( Body('c3', 100.0, glm.vec3(10.0, 20.0, 10.0)))
    universo.listBody.append( Body('c4', 100.0, glm.vec3(10.0, 5.0, 10.0)))
    universo.listBody.append( Body('c4', 100.0, glm.vec3(-10.0, -10.0, -10.0)))

    print('Universo:{0}' .format(universo))