#!/usr/bin/env python3
'''
Created on 20160921
Update on 20191105
@author: Eduardo Pagotto
 '''

import math
import glm
   
class Body(object):
    def __init__(self, nome, massa = 0.0, cor = glm.vec4(), posicao = glm.vec3(), velocidade = glm.vec3()):
        self.nome = nome
        self.massa = massa
        self.posicao = posicao
        self.velocidade = velocidade
        self.lastTime = 0
        self.aceleracao = glm.vec3()
        self.accForce = glm.vec3()
        self.cor = cor
        self.enable = True

    def __str__(self):
        return str('Nome:{0}, Massa:{1} Pos:{2} Vel:{3}' .format(self.nome, self.massa, self.posicao, self.velocidade))

    def calcNeighborAcc(self, neighbor):
        #Distancia entre G e g
        distance = glm.distance(self.posicao, neighbor.posicao)

        #calculo da forca escalar Fg = G (M1 * M2 / d **2)
        escalarForce = 6.67e-11 * ((self.massa * neighbor.massa) / (distance **2))

        #proporcao (Regra de 3), da forca em cada eixo
        self.accForce += (( neighbor.posicao - self.posicao) * escalarForce ) / distance 

    def accelerateAcc(self, ticktackCount):
        
        self.aceleracao = self.accForce / self.massa # a = F / m
        self.velocidade += (self.aceleracao * ticktackCount)  # V = Vo * at
        self.posicao += self.velocidade              # S = So + V
        self.lastTime = ticktackCount
        self.accForce = glm.vec3()

    def impact(self, force):
        self.accForce = force
        # self.aceleracao = force / self.massa # a = F / m
        # self.velocidade += self.aceleracao  # V = Vo * at
        # self.posicao += self.velocidade              # S = So + V
        # self.lastTime = ticktackCount;
        # self.accForce = Vec3()

    def calcForce(self):
        return self.aceleracao * self.massa

    def near(self, neighbor, minDistance):
        distance = glm.distance(self.posicao, neighbor.posicao)
        if distance < minDistance:
            return True
        
        return False
            
if __name__ == '__main__':

    body1 = Body('corpo1', 1000.0)
    body2 = Body('corpo2', 1000.0, glm.vec4(), glm.vec3(1.0, 1.0, 1.0))

    print('Corpo:{0}'.format(body1))
    print('Corpo:{0}'.format(body2))
