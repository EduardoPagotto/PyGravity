#!/usr/bin/env python3
'''
Created on 20200131
Update on 20200131
@author: Eduardo Pagotto
 '''

from PyGravity.core.Canvas import Canvas
from PyGravity.core.FlowControl import FlowControl
#from PyGravity.core.IClient import IClient
from PyGravity.core.ClientBase import ClientBase

import sdl2

if __name__ == '__main__':

    sdl2.SDL_LogSetAllPriority(sdl2.SDL_LOG_PRIORITY_DEBUG)
    sdl2.SDL_Log(b"App Iniciado")

    canvas = Canvas("teste", 640, 480)

    client = ClientBase(canvas)

    flow = FlowControl(client)
    flow.loop()

    sdl2.SDL_Log(b"App Finalizado")

