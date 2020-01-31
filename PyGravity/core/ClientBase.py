#!/usr/bin/env python3
'''
Created on 20200131
Update on 20200131
@author: Eduardo Pagotto
'''

import ctypes
import sdl2

from PyGravity.core.IClient import IClient

class ClientBase(IClient):
    def __init__(self, canvas):
        self.canvas = canvas
        self.pause = False

    def start(self):
        return

    def stop(self):
        return

    def render(self):
        return

    def keyCapture(self, tecla):

        if tecla == sdl2.SDLK_ESCAPE:
            self.pause = True
            event = sdl2.SDL_Event()
            event.type = sdl2.SDL_QUIT
            if sdl2.SDL_PushEvent(event) == -1:
                raise Exception(sdl2.SDL_GetError().encode())
        elif tecla == sdl2.SDLK_F10:
            pass
            #Chimera::eventsSend(Chimera::KindOp::VIDEO_TOGGLE_FULL_SCREEN, nullptr, nullptr);
        else:
            pass

    def mouseButtonDownCapture(self, mb):
        return

    def mouseButtonUpCapture(self, mb):
        return

    def mouseMotionCapture(self, mb):
        return

    def joystickCapture(self, joy):
        return

    def joystickStatus(self, joy):
        return

    def userEvent(self, _event):
        return

    def newFPS(self, fps):
        return

    def windowEvent(self, _event):
        return

    def paused(self):
        return self.pause