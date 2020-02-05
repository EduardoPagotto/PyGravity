#!/usr/bin/env python3
'''
Created on 20200205
Update on 20200205
@author: Eduardo Pagotto
'''

import math
import sdl2

class Joystick(object):
    def __init__(self):
        self.id = 0
        self.name = None
        self.pJoystick = None

        self.Axes = {}
        self.Hats = {}
        self.BallsX = {}
        self.BallsY = {}
        self.ButtonsDown = {}

    def AxisScale(self, value):
        return value / 32767.0 if value > 0 else value / 32768.0

    def AxisScaled(self, axis, low, high, deadzone = 0.0,  deadzone_at_ends = 0.0):
        return low + (high - low) * (self.Axis(axis, deadzone, deadzone_at_ends) + 1.0) / 2.0
    
    def Axis(self, axis, deadzone, deadzone_at_ends):
        if axis in self.Axes:
            value = self.Axes[axis]
            if math.fabs(value) < deadzone:
                return 0.0
            elif value + deadzone_at_ends > 1.0:
                return 1.0
            elif value - deadzone_at_ends < -1.0:
                return -1.0
            else:
                # Reclaim the range of values lost to the deadzones.
                if value > 0.0:
                    value -= deadzone
                else:
                    value += deadzone
                
                value /= (1.0 - deadzone - deadzone_at_ends)
    
            return value
    
        return 0.0

    def ButtonDown(self, button):
        if button in self.ButtonsDown:
            return self.ButtonsDown[button]

        return False

    def Hat(self, hat): 
        # Check the direction of a hat switch.
        if hat in self.Hats:
            return self.Hats[hat]

        return 0

    def TrackEvent(self, event):

        val = event.type   

        if val == sdl2.SDL_JOYAXISMOTION:
            self.Axes[event.jaxis.axis] = self.AxisScale(event.jaxis.value)
        elif val == sdl2.SDL_JOYBUTTONDOWN:
            self.ButtonsDown[event.jbutton.button] = True
        elif val == sdl2.SDL_JOYBUTTONUP:
            self.ButtonsDown[event.jbutton.button] = False
        elif val == sdl2.SDL_JOYHATMOTION:
            self.Hats[event.jhat.hat] = event.jhat.value
        elif val == sdl2.SDL_JOYBALLMOTION:
            self.BallsX[event.jball.ball] += event.jball.xrel
            self.BallsY[event.jball.ball] += event.jball.yrel
