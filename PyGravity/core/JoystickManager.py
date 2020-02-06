#!/usr/bin/env python3
'''
Created on 20200205
Update on 20200205
@author: Eduardo Pagotto
'''

import sdl2

class JoystickManager(object):
    def __init__(self):
        self.Joysticks = {}
        self.initialized = False

    def __del__(self):
        if self.initialized is True:
            self.ReleaseJoysticks()
            sdl2.SDL_JoystickEventState(sdl2.SDL_DISABLE)
            sdl2.SDL_QuitSubSystem(sdl2.SDL_INIT_JOYSTICK)
    
        self.initialized = False

    def Initialize(self):
        if not self.initialized:
            sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_JOYSTICK)
            sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)

        self.initialized = True

    def ReleaseJoysticks(self):

        if not self.initialized:
            return

        for _, joy in self.Joysticks:

            if joy.pJoystick is not None:
                sdl2.SDL_JoystickClose(joy.pJoystick)
                joy.pJoystick = None
                joy.name = 'Disconnected'

        self.Joysticks = {}


    def FindJoysticks(self):

        if not self.initialized:
            return

        for i in range(sdl2.SDL_NumJoysticks()):
            if self.Joysticks[i].pJoystick is not None:
                self.Joysticks[i].id = i
                self.Joysticks[i].pJoystick = sdl2.SDL_JoystickOpen(i)
                if self.Joysticks[i].pJoystick is not None:
                    name = sdl2.SDL_JoystickName(self.Joysticks[i].pJoystick)
                    self.Joysticks[i].name = name if name is not None else 'Joystick'


    def getJoystickState(self, joystick_id):
        if joystick_id in self.Joysticks:
            return self.Joysticks[joystick_id]

        return None

    
    def TrackEvent(self, event):
        id = 255
        if event.type ==  sdl2.SDL_JOYAXISMOTION:
            id = event.jaxis.which
        if event.type ==  sdl2.SDL_JOYBUTTONDOWN or event.type ==  sdl2.SDL_JOYBUTTONUP:
            id = event.jbutton.which
        if event.type ==  sdl2.SDL_JOYHATMOTION:
            id = event.jhat.which
        if event.type ==  sdl2.SDL_JOYBALLMOTION:
            id = event.jball.which
        if event.type ==  sdl2.SDL_JOYDEVICEADDED or event.type ==  sdl2.SDL_JOYDEVICEREMOVED:
            self.FindJoysticks()
        else:
            return False
    
        self.Joysticks[id].id = id
        self.Joysticks[id].TrackEvent(event)
        return True
