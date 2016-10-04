'''
Created on 21 de set de 2016

@author: pagotto
'''
import math

class Color(object):
    def __init__(self,r=1.0, g=1.0, b=1.0, a=1.0):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    @staticmethod
    def RED():
        return Color(1.0, 0.0, 0.0, 1.0)

    @staticmethod
    def GREEN():
        return Color(0.0, 1.0, 0.0, 1.0)

    @staticmethod
    def BLUE():
        return Color(0.0, 0.0, 1.0, 1.0)

    @staticmethod
    def YELLOW():
        return Color(1.0, 1.0, 0.0, 1.0)

class Vec3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        
    def distance(self, posicao):
        return math.sqrt( math.pow( ( self.x - posicao.x ),2 ) + math.pow( ( self.y - posicao.y ),2 ) + math.pow( ( self.z - posicao.z ),2 ))

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __str__(self):
        return str('{valx},{valy},{valz}'.format(valx = self.x, valy = self.y, valz = self.z))        
        
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

    def calcNeighbor(self, neighbor):
        distance = self.posicao.distance(neighbor.posicao)
        escalarForce = 6.67e-11 * self.massa * neighbor.massa / math.pow(distance,2)
        return Vec3((escalarForce * ( neighbor.posicao.x - self.posicao.x ) / distance), 
                     (escalarForce * ( neighbor.posicao.y - self.posicao.y ) / distance),
                     (escalarForce * ( neighbor.posicao.z - self.posicao.z ) / distance))

    def calcNeighborAcc(self, neighbor):
        distance = self.posicao.distance(neighbor.posicao)
        escalarForce = 6.67e-11 * self.massa * neighbor.massa / math.pow(distance,2)
        self.accForce.add( Vec3((escalarForce * ( neighbor.posicao.x - self.posicao.x ) / distance), 
                                (escalarForce * ( neighbor.posicao.y - self.posicao.y ) / distance),
                                (escalarForce * ( neighbor.posicao.z - self.posicao.z ) / distance)))

    def accelerate(self, force, time):
        self.aceleracao = Vec3(force.x / self.massa,
                                force.y / self.massa,
                                force.z / self.massa)
        self.velocidade = Vec3(self.velocidade.x + self.aceleracao.x * time, 
                                self.velocidade.y + self.aceleracao.y * time, 
                                self.velocidade.z + self.aceleracao.z * time)
        self.posicao = Vec3(self.posicao.x + self.velocidade.x, 
                            self.posicao.y + self.velocidade.y, 
                            self.posicao.z + self.velocidade.z)
        self.lastTime = time;

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

    def __str__(self):
        return str('Nome:{0}, Massa:{1} Pos:{2} Vel:{3}' .format(self.nome, self.massa, self.posicao, self.velocidade))

if __name__ == '__main__':

    body1 = Body('corpo1', 1000.0)
    body2 = Body('corpo2', 1000.0, Color(), Vec3(1.0, 1.0, 1.0))

    print('Corpo:{0}'.format(body1))
    print('Corpo:{0}'.format(body2))

    #body2.calcNeighborAcc(body1);
    body1.accelerate(Vec3(5.0, 5.0, 5.0), 10)