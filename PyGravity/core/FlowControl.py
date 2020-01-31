#!/usr/bin/env python3
'''
Created on 20200131
Update on 20200131
@author: Eduardo Pagotto
'''

import ctypes
import sdl2

class FlowControl(object):
    def __init__(self, client):
        self.client = client
        self.currentFPS = 0

    def __del__(self):
        sdl2.SDL_Quit()

    def open(self):
        #joystickManager.Initialize()
        #joystickManager.FindJoysticks()
        self.client.start()

    def close(self):
        #joystickManager.ReleaseJoysticks()
        event = sdl2.SDL_Event()
        event.type = sdl2.SDL_QUIT
        if sdl2.SDL_PushEvent(event) == -1:
            raise Exception(sdl2.SDL_GetError().decode())

    def __execute(self):
        try:
            #self.countFrame()
            self.client.render()
            #self.client.joystickStatus(joystickManager)
        except:
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
                    # if joystickManager.TrackEvent(event) is True:
                    #     self.client.joystickCapture(joystickManager)
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
                sdl2.SDL_LogDebug(sdl2.SDL_LOG_CATEGORY_RENDER, b"DeltaTime: %d  Delay: %d", deltaTime, tot_delay)
                sdl2.SDL_Delay(tot_delay)
            else:
                sdl2.SDL_LogDebug(sdl2.SDL_LOG_CATEGORY_RENDER, b"DeltaTime: %d TimeElapsed: %d", deltaTime, timeElapsed)


            