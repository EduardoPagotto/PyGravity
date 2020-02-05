#!/usr/bin/env python3
'''
Created on 20200131
Update on 20200131
@author: Eduardo Pagotto
'''

import ctypes
import sdl2
from OpenGL import GL as gl

class Canvas(object):
    def __init__(self, _title,  _width,  _height, _fullScreen = False):

        self.title = _title
        self.width = _width
        self.height = _height
        self.fullScreen = _fullScreen

        # Init
        if sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING) != 0:
            raise Exception(sdl2.SDL_GetError().decode())

        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 2)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)

        self.window = sdl2.SDL_CreateWindow(self.title.encode(),
                                            sdl2.SDL_WINDOWPOS_UNDEFINED,
                                            sdl2.SDL_WINDOWPOS_UNDEFINED, 
                                            self.width, 
                                            self.height,
                                            sdl2.SDL_WINDOW_OPENGL| sdl2.SDL_WINDOW_SHOWN)

        if not self.window:
            raise Exception("Error: Could not create window: %s", sdl2.SDL_GetError().decode())
        
        self.glcontext = sdl2.SDL_GL_CreateContext(self.window)

        interval = sdl2.SDL_GL_SetSwapInterval(1)
        if interval < 0:
            msg = sdl2.SDL_GetError().decode()
            raise Exception("Falha ao Ajustar o VSync:" + msg)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        #gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable(gl.GL_CULL_FACE)
        #gl.glEnable(gl.GL_BLEND)
        #gl.glClearColor(0.3, 0.3, 0.3, 1.0)

    def initGL(self):
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_BLEND)

    def destroy(self):
        sdl2.SDL_GL_DeleteContext(self.glcontext)
        sdl2.SDL_DestroyWindow(self.window)

    def before(self):
        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def after(self):
        sdl2.SDL_GL_SwapWindow(self.window)