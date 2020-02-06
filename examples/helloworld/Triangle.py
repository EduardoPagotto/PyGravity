#!/usr/bin/env python3
'''
Created on 202002204
Update on 202002204
@author: Eduardo Pagotto
'''

import numpy
import ctypes
import array
import struct

from OpenGL.GL import *

from PyGravity.core.VBO import VBO 
from PyGravity.core.IBO import IBO
from PyGravity.core.Shader import Shader

class Triangle:
    def __init__(self) -> None:
        self.vbo: VBO = None
        self.ibo: IBO = None
        self.shader: Shader = None

        self.vao = None

        #self.positions = (-1.0, -1.0, 1.0, -1.0, 0.0, 1.0)
        #self.indices = (0, 1, 2)

    def initialize(self):
        self.shader = Shader()

        VS = None
        with open('./shaders/helloworld.vert') as f:
            VS = f.read()

        FS = None
        with open('./shaders/helloworld.frag') as f:
            FS = f.read()
       
        self.shader.compile(VS, FS)

        vertexData = numpy.array([
        # Vertex Positions
            0.0, 0.5, 0.0, 1.0,
            0.5, -0.366, 0.0, 1.0,
            -0.5, -0.366, 0.0, 1.0,

        # Vertex Colours
            1.0, 0.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 1.0,
        ], dtype=numpy.float32)

        # Core OpenGL requires that at least one OpenGL vertex array be bound
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)


        self.vbo = VBO()
        self.ibo = IBO()

        # if False:
        #     # Error
        #     self.vbo.set_vertex_attribute(2, 4 * 2 * 3,
        #                                   array.array('f', self.positions))
        #     self.ibo.set_indices(4, 12, array.array('I', self.indices))
        # elif True:
        #     # OK
        #     self.vbo.set_vertex_attribute(2, 4 * 2 * 3, (ctypes.c_float *
        #                                                  6)(*self.positions))
        #     self.ibo.set_indices(4, 12, (ctypes.c_uint * 3)(*self.indices))
        # elif False:
        #     # not work
        #     self.vbo.set_vertex_attribute(2, 4 * 2 * 3,
        #                                  memoryview(struct.pack("6f", *self.positions)))
        #     self.ibo.set_indices(4, 12, memoryview(struct.pack("3I", *self.indices)))

        # else:
        #     # OK
        #     self.vbo.set_vertex_attribute(2, 4 * 2 * 3,
        #                                  struct.pack("6f", *self.positions))
        #     self.ibo.set_indices(4, 12, struct.pack("3I", *self.indices))

    def draw(self) -> None:
        self.shader.use()
        self.vbo.set_slot(0)
        self.ibo.bind()
        self.ibo.draw()

        self.ibo.unbind()
        self.vbo.unbind()
        self.shader.unuse()