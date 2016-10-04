'''
Created on 21 de set de 2016

@author: pagotto
'''
from Body import Body
from Body import vec3
from Universe import Universe
from Gravitacao import Gravitacao

from time import sleep
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = 'ball_glut'
universo = Universe(vec3(100.0, 100.0, 100.0))
grav = Gravitacao(universo)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutCreateWindow(name)

    glClearColor(0.,0.,0.,1.)
    glShadeModel(GL_SMOOTH)
    #glShadeModel(GL_FLAT)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10.,4.,140.,0.0]#[10.,4.,10.,1.]
    lightZeroColor = [1.0,1.0,1.0,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,500.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,250,
              0,0,0,
              0,1,0)
    glPushMatrix()
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    #color = [1.0,0.,0.,1.]
    #glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    #glutSolidSphere(1,10,10)
    desenhaCorpos()
    glPopMatrix()
    glutSwapBuffers()

    grav.step()

    return

def desenhaCorpos():    
    tot = len(universo.listBody)
    for indice in range(0, tot):
        posiciona(indice)

def posiciona(indice):
    glPushMatrix()
    corpo = universo.listBody[indice]
    glColor( corpo.cor.x, corpo.cor.y, corpo.cor.z)
    glTranslatef(corpo.posicao.x, corpo.posicao.y, corpo.posicao.z)
    #print('{0}'.format( corpo ))
    glutSolidSphere(2,10,10)
    glPopMatrix()
    
if __name__ == '__main__':
     
    universo.listBody.append( Body('c1', 5000.0, vec3(10.0, 0.0, 0.0), vec3(0.0, 0.05, 0.0)))
    universo.listBody.append( Body('c2', 155000.0, vec3(0.0, 0.0, 0.0)))
    universo.listBody.append( Body('c3', 100.0, vec3(70.0, 70.0, 0.0))) 
    universo.listBody.append( Body('c4', 100.0, vec3(-70.0, -70.0, 0.0), vec3(0.003, 0.0, 0.0))) 
    universo.listBody.append( Body('c5', 10.0, vec3(70.0, -70.0, 0.0), vec3(0.0, 0.0, 0.0)))
    universo.listBody.append( Body('c6', 1.0, vec3(-50.0, 70.0, 0.0), vec3(0.0, 0.0, 0.0))) 
    universo.listBody.append( Body('c7', 1.0, vec3(-70.0, 50.0, 0.0), vec3(0.0, 0.0, 0.0))) 
    universo.listBody.append( Body('c8', 3.0, vec3(-70.0, 20.0, 0.0), vec3(0.0, 0.0, 0.0))) 
    universo.listBody.append( Body('c9', 1.0, vec3(-79.0, 70.0, 0.0), vec3(0.0, 0.0, 0.0))) 
    universo.listBody.append( Body('c10', 5.0, vec3(-70.0, 70.0, 0.0), vec3(0.0, 0.0, 0.0))) 

    main()

    #universo = Universe(vec3(100.0, 100.0, 100.0))
    #universo.listBody.append( Body('c1', 10000.0, vec3(5.0, 5.0, 0.0)))
    
    # universo.listBody.append( Body('c3', 10000.0, vec3(10.0, 20.0, 10.0)))
    # universo.listBody.append( Body('c4', 10000.0, vec3(10.0, 5.0, 10.0)))
    # universo.listBody.append( Body('c4', 10000.0, vec3(-10.0, -10.0, -10.0)))

    #grav = Gravitacao(universo)
    # tot = len(universo.listBody)

    # while True:
    #     for indice in range(0, tot):
    #         print('{0}'.format( universo.listBody[indice] ))

    #     grav.step()

    #     sleep(0.1)
    #     print('-------------------')
    #     sys.stdout.flush()