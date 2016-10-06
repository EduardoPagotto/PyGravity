'''
Created on 21 de set de 2016

@author: pagotto
'''

from Body import Body
from Body import Vec3
from Body import Color
from Universe import Universe

from time import sleep
import sys

class Gravitacao(object):
    def __init__(self, universo):
        self.universo = universo
        self.time = 1500

    def step(self):
        tot = len(self.universo.listBody)
        for indiceA in range(0, tot):
            corpoA = self.universo.listBody[indiceA]

            if corpoA.enable == False:
                continue

            for indiceB in range(0, tot):
                corpoB = self.universo.listBody[indiceB]

                if corpoB.enable == False:
                    continue
                
                if indiceA != indiceB:
                    corpoA.calcNeighborAcc(corpoB)
                    #impacto de corpos 
                    if corpoA.near(corpoB, 1.0):
                        #calcula a forca
                        forcaA = corpoA.calcForce()
                        forcaB = corpoB.calcForce()
                        #remove o corpo de menor massa
                        if corpoA.massa >= corpoB.massa:
                            corpoA.massa += corpoB.massa
                            corpoA.impact(forcaB)
                            corpoB.enable = False
                            #self.universo.listBody.remove(corpoB)
                        else:
                            corpoB.impact(forcaA)
                            corpoB.massa += corpoA.massa
                            corpoA.enable = False
                            #self.universo.listBody.remove(corpoA)

                corpoA.accelerateAcc(self.time)
                
                if self.universo.isInside(corpoA.posicao) != True:
                    corpoA.enable = False

if __name__ == '__main__':
    
    universo = Universe(Vec3(100.0, 100.0, 100.0))
    universo.listBody.append( Body('c1', 10000.0, Color(), Vec3(10.0, 10.0, 0.0)))
    universo.listBody.append( Body('c2', 10000.0, Color(), Vec3(0.0, 0.0, 0.0)))
    # universo.listBody.append( Body('c3', 10000.0, vec3(10.0, 20.0, 10.0)))
    # universo.listBody.append( Body('c4', 10000.0, vec3(10.0, 5.0, 10.0)))
    # universo.listBody.append( Body('c4', 10000.0, vec3(-10.0, -10.0, -10.0)))

    grav = Gravitacao(universo)
    tot = len(universo.listBody)

    while True:
        for indice in range(0, tot):
            print('{0}'.format( universo.listBody[indice] ))

        grav.step()

        sleep(0.1)
        print('-------------------')
        sys.stdout.flush()
