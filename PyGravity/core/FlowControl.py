#!/usr/bin/env python3
'''
Created on 20200131
Update on 20200131
@author: Eduardo Pagotto
'''

import ctypes
import sdl2

from PyGravity.core.JoystickManager import JoystickManager

class FlowControl(object):
    def __init__(self, client):
        self.client = client
        self.currentFPS = 0

        self.joystickManager = JoystickManager()
        self.joystickManager.Initialize()
        self.joystickManager.FindJoysticks()
        self.client.start()

    def __execute(self):
        try:
            #self.countFrame()
            self.client.render()
            self.client.joystickStatus(self.joystickManager)
        except Exception as exp:
            sdl2.SDL_LogError(sdl2.SDL_LOG_CATEGORY_RENDER, str(exp).encode())
            sdl2.SDL_Quit()

    def loop(self):

        timeElapsed = 0
        tot_delay = 0
        lastFrameTime = 0
        deltaTime = 0
        fpsMin = 60.0
        minimumFrameTime = 1000.0 / fpsMin

        running = True
        event = sdl2.SDL_Event()
        while running:

            frameTime = sdl2.SDL_GetTicks()

            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    self.client.stop()

                elif event.type == sdl2.SDL_KEYDOWN:
                    self.client.keyCapture(event.key.keysym.sym)

                elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    self.client.mouseButtonDownCapture(event.button)

                elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                    self.client.mouseButtonUpCapture(event.button)

                elif event.type == sdl2.SDL_MOUSEMOTION:
                    self.client.mouseMotionCapture(event.motion)

                elif event.type == sdl2.SDL_USEREVENT:
                    self.client.userEvent(event)

                elif event.type == sdl2.SDL_WINDOWEVENT:
                    self.client.windowEvent(event)

                else:
                    if self.joystickManager.TrackEvent(event) is True:
                        self.client.joystickCapture(self.joystickManager)
                    pass

            if self.client.paused() is False:
                self.__execute() # Se nao houver foco na tela pule o render

            # inicio contadores
            deltaTime = frameTime - lastFrameTime
            lastFrameTime = frameTime

            self.currentFPS = 1000 / deltaTime

            timeElapsed = (sdl2.SDL_GetTicks() - frameTime)
            if timeElapsed < minimumFrameTime:
                tot_delay = minimumFrameTime - timeElapsed
                #sdl2.SDL_LogDebug(sdl2.SDL_LOG_CATEGORY_RENDER, "DeltaTime:{0} Delay:{1}".format(deltaTime, tot_delay).encode())
                sdl2.SDL_Delay(ctypes.c_uint(int(tot_delay)))
            else:
                pass
                #sdl2.SDL_LogDebug(sdl2.SDL_LOG_CATEGORY_RENDER, "DeltaTime: {0} TimeElapsed: {1}".format(deltaTime, timeElapsed).encode())


            