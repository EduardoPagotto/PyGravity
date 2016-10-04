'''
Created on 21 de set de 2016

@author: pagotto
'''

from Body import Body
from Body import vec3
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

            for indiceB in range(0, tot):
                corpoB = self.universo.listBody[indiceB]
                if indiceA != indiceB:
                    corpoA.calcNeighborAcc(corpoB)
            
            corpoA.accelerateAcc(self.time)

if __name__ == '__main__':
    
    universo = Universe(vec3(100.0, 100.0, 100.0))
    universo.listBody.append( Body('c1', 10000.0, vec3(10.0, 10.0, 0.0)))
    universo.listBody.append( Body('c2', 10000.0, vec3(0.0, 0.0, 0.0)))
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
