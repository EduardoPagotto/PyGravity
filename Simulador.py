#!/usr/bin/env python3
'''
Created on 20160921
Update on 20191105
@author: Eduardo Pagotto
 '''

import sys
import glm
from Body import Body
from Universe import Universe
from Gravitacao import Gravitacao
from time import sleep
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

def RED():
    return glm.vec4(1.0, 0.0, 0.0, 1.0)

def GREEN():
    return glm.vec4(0.0, 1.0, 0.0, 1.0)

def BLUE():
    return glm.vec4(0.0, 0.0, 1.0, 1.0)

def YELLOW():
    return glm.vec4(1.0, 1.0, 0.0, 1.0)

name = 'Gravitacao N-to-N'
universo = Universe(300.0)
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
    gluLookAt(0,0,400,
              0,0,0,
              0,1,0)
    glPushMatrix()
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
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
    
    corpo = universo.listBody[indice]
    if corpo.enable == True:
        glPushMatrix()
        color = [corpo.cor.r, corpo.cor.g, corpo.cor.b, corpo.cor.a] 
        glMaterialfv(GL_FRONT,GL_DIFFUSE, color)
        glTranslatef(corpo.posicao.x, corpo.posicao.y, corpo.posicao.z)
        #print('{0}'.format( corpo ))
        glutSolidSphere(2,10,10)
        glPopMatrix()
    
if __name__ == '__main__':
    
    #universo.listBody.append( Body('c1', 200000.0, RED(), glm.vec3(50.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 0.0)))
    #universo.listBody.append( Body('c1', 200000.0, BLUE(), glm.vec3(-50.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 0.0)))

    # universo.listBody.append( Body('c1', 100.0, Color.BLUE(), glm.vec3(-50.0, 70.0, 0.0), glm.vec3(0.0, -0.01, 0.0))) 
    # universo.listBody.append( Body('c3', 100.0, BLUE(), glm.vec3(-79.0, 70.0, 0.0), glm.vec3(0.0, -0.01, 0.0))) 
    # universo.listBody.append( Body('c4', 200.0, RED(), glm.vec3(-70.0, -20.0, 0.0), glm.vec3(0.0, -0.01, 0.0))) 
    # universo.listBody.append( Body('c6', 200.0, Color.RED(), glm.vec3(70.0, -70.0, 0.0), glm.vec3(0.0, -0.01, 0.0)))     
    # universo.listBody.append( Body('c7', 400.0, GREEN(), glm.vec3(70.0, 70.0, 0.0))) 
    # universo.listBody.append( Body('c8', 400.0, GREEN(), glm.vec3(-70.0, -70.0, 0.0), glm.vec3(0.0, 0.0, 0.0))) 
    universo.listBody.append( Body('c9', 8000.0, YELLOW(), glm.vec3(-30.0, 90.0, 0.0), glm.vec3(0.0, 0.02, 0.0)))
    universo.listBody.append( Body('c9', 8000.0, YELLOW(), glm.vec3(30.0, -90.0, 0.0), glm.vec3(0.0, -0.025, 0.0)))
    universo.listBody.append( Body('ca', 200000.0, glm.vec4(), glm.vec3(-50.0, 90.0, 0.0), glm.vec3(0.0, -0.001, 0.0)))
    universo.listBody.append( Body('ca', 200000.0, glm.vec4(), glm.vec3(50.0, -90.0, 0.0), glm.vec3(0.0, 0.001, 0.0)))
    universo.listBody.append( Body('ca', 8000.0, BLUE(), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.01, 0.0, 0.0)))

    main()
