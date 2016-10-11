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
        self.ticktack = 21500

    def processaColisao(self, corpoA, corpoB):
        #impacto de corpos 
        if corpoA.near(corpoB, 2.0):
            #calcula a forca
            forcaA = corpoA.calcForce()
            forcaB = corpoB.calcForce()

            amplitudeForcaA = forcaA.module()
            amplitudeForcaB = forcaB.module()
            forcaResultante = Vec3()

            if amplitudeForcaA > amplitudeForcaB:
                forcaResultante = forcaA - forcaB
            else:
                forcaResultante = forcaB - forcaA

            #remove o corpo de menor massa
            if corpoA.massa >= corpoB.massa:
                corpoA.massa += corpoB.massa
                #corpoA.aceleracao = forcaResultante.divisor( corpoA.massa )
                corpoA.impact(forcaResultante)
                corpoB.enable = False
            else:
                corpoB.massa += corpoA.massa
                #corpoB.aceleracao = forcaResultante / corpoB.massa
                corpoB.impact(forcaResultante)
                corpoA.enable = False

    def somatoriaForcas(self, numeroCorpos):
        for indiceA in range(0, numeroCorpos):
            corpoA = self.universo.listBody[indiceA]

            #Se corpo esta invalido (colidiu com outro corpo ou fora do universo)
            if corpoA.enable == False:
                continue

            for indiceB in range(0, numeroCorpos):
                corpoB = self.universo.listBody[indiceB]

                #Se corpo esta invalido (colidiu com outro corpo ou fora do universo)
                if corpoB.enable == False:
                    continue
                
                if indiceA != indiceB:
                    #acumula forca dos visinhos
                    corpoA.calcNeighborAcc(corpoB)

            #executa a somatoria das forcas visinha e zera acumulador de forca
            corpoA.accelerateAcc(self.ticktack)

    def colisao(self, numeroCorpos):
        for indiceA in range(0, numeroCorpos):
            corpoA = self.universo.listBody[indiceA]

            #Se corpo esta invalido (colidiu com outro corpo ou fora do universo)
            if corpoA.enable == False:
                continue

            for indiceB in range(0, numeroCorpos):
                corpoB = self.universo.listBody[indiceB]

                #Se corpo esta invalido (colidiu com outro corpo ou fora do universo)
                if corpoB.enable == False:
                    continue
                
                if indiceA != indiceB:
                    self.processaColisao(corpoA, corpoB)
            
            if self.universo.isInside(corpoA.posicao) != True:
                corpoA.enable = False

    def step(self):
        tot = len(self.universo.listBody)

        self.somatoriaForcas(tot)
        self.colisao(tot)   
        #verifica se corpo ainda esta no limite do universo
        #if self.universo.isInside(corpoA.posicao) != True:
        #    corpoA.enable = False

if __name__ == '__main__':
    
    universo = Universe(100.0)
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
