#!/usr/bin/env python3
'''
Created on 20200206
Update on 20200206
@author: Eduardo Pagotto
'''

import ctypes
import sdl2

from PyGravity.core.IClient import IClient

from Triangle import Triangle

class Game(IClient):
    def __init__(self, canvas):
        self.canvas = canvas
        self.pause = False

        self.triangle = Triangle()

    def start(self):
        self.canvas.initGL()

        self.triangle.initialize()

    def stop(self):
        self.canvas.destroy()

    def render(self):
        self.canvas.before()

        # TODO desenhar aqui!!
        # sdl2.SDL_Delay(ctypes.c_uint(5))
        self.triangle.draw()

        self.canvas.after()


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
        if _event.window.event == sdl2.SDL_WINDOWEVENT_ENTER:
            self.pause = False
            sdl2.SDL_LogDebug(sdl2.SDL_LOG_CATEGORY_RENDER, b"Resume..")
        elif _event.window.event == sdl2.SDL_WINDOWEVENT_LEAVE:
            self.pause = True
            sdl2.SDL_LogDebug(sdl2.SDL_LOG_CATEGORY_RENDER, b"Pause..")
        elif _event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
            #pVideo->reshape(_event.data1, _event.data2);
            pass
        else:
            pass
    
    def paused(self):
        return self.pause