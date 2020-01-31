#!/usr/bin/env python3
'''
Created on 20200131
Update on 20200131
@author: Eduardo Pagotto
'''

import abc

class IClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self):
        return

    @abc.abstractmethod
    def stop(self):
        return

    @abc.abstractmethod
    def render(self):
        return

    @abc.abstractmethod
    def keyCapture(self, tecla):
        return

    @abc.abstractmethod
    def mouseButtonDownCapture(self, mb):
        return

    @abc.abstractmethod
    def mouseButtonUpCapture(self, mb):
        return

    @abc.abstractmethod
    def mouseMotionCapture(self, mb):
        return

    @abc.abstractmethod
    def joystickCapture(self, joy):
        return

    @abc.abstractmethod
    def joystickStatus(self, joy):
        return

    @abc.abstractmethod
    def userEvent(self, _event):
        return

    @abc.abstractmethod
    def newFPS(self, fps):
        return

    @abc.abstractmethod
    def windowEvent(self, _event):
        return

    @abc.abstractmethod
    def paused(self):
        return
