'''
Created on 21 de set de 2016

@author: pagotto
'''
import math
from Color import Color
from Vec3 import Vec3
        
class Body(object):
    def __init__(self, nome, massa = 0.0, cor = Color(), posicao = Vec3(), velocidade= Vec3()):
        self.nome = nome
        self.massa = massa
        self.posicao = posicao
        self.velocidade = velocidade
        self.lastTime = 0
        self.aceleracao = Vec3()
        self.accForce = Vec3()
        self.cor = cor
        self.enable = True

    def __str__(self):
        return str('Nome:{0}, Massa:{1} Pos:{2} Vel:{3}' .format(self.nome, self.massa, self.posicao, self.velocidade))

    def calcNeighborAcc(self, neighbor):
        distance = self.posicao.distance(neighbor.posicao)
        escalarForce = 6.67e-11 * self.massa * neighbor.massa / math.pow(distance,2)
        self.accForce.add( Vec3((escalarForce * ( neighbor.posicao.x - self.posicao.x ) / distance), 
                                (escalarForce * ( neighbor.posicao.y - self.posicao.y ) / distance),
                                (escalarForce * ( neighbor.posicao.z - self.posicao.z ) / distance)))

    def accelerateAcc(self, time):
        self.aceleracao = Vec3(self.accForce.x / self.massa, 
                                self.accForce.y / self.massa, 
                                self.accForce.z / self.massa)
        self.velocidade = Vec3(self.velocidade.x + self.aceleracao.x * time, 
                                self.velocidade.y + self.aceleracao.y * time, 
                                self.velocidade.z + self.aceleracao.z * time)
        self.posicao = Vec3(self.posicao.x + self.velocidade.x, 
                            self.posicao.y + self.velocidade.y, 
                            self.posicao.z + self.velocidade.z)
        self.lastTime = time;
        self.accForce = Vec3()

    def impact(self, force):
        self.accForce.add(force)

    def calcForce(self):
        return self.aceleracao.prod(self.massa)

    def near(self, neighbor, minDistance):
        distance = self.posicao.distance(neighbor.posicao)
        if distance < minDistance:
            return True
        
        return False


    # def calcNeighbor(self, neighbor):
    #     distance = self.posicao.distance(neighbor.posicao)
    #     escalarForce = 6.67e-11 * self.massa * neighbor.massa / math.pow(distance,2)
    #     return Vec3((escalarForce * ( neighbor.posicao.x - self.posicao.x ) / distance), 
    #                  (escalarForce * ( neighbor.posicao.y - self.posicao.y ) / distance),
    #                  (escalarForce * ( neighbor.posicao.z - self.posicao.z ) / distance))

    # def accelerate(self, force, time):
    #     self.aceleracao = Vec3(force.x / self.massa,
    #                             force.y / self.massa,
    #                             force.z / self.massa)
    #     self.velocidade = Vec3(self.velocidade.x + self.aceleracao.x * time, 
    #                             self.velocidade.y + self.aceleracao.y * time, 
    #                             self.velocidade.z + self.aceleracao.z * time)
    #     self.posicao = Vec3(self.posicao.x + self.velocidade.x, 
    #                         self.posicao.y + self.velocidade.y, 
    #                         self.posicao.z + self.velocidade.z)
    #     self.lastTime = time;
            

if __name__ == '__main__':

    body1 = Body('corpo1', 1000.0)
    body2 = Body('corpo2', 1000.0, Color(), Vec3(1.0, 1.0, 1.0))

    print('Corpo:{0}'.format(body1))
    print('Corpo:{0}'.format(body2))

    #body2.calcNeighborAcc(body1);
    #body1.accelerate(Vec3(5.0, 5.0, 5.0), 10)