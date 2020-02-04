#!/usr/bin/env python3
'''
Created on 202002204
Update on 202002204
@author: Eduardo Pagotto
'''

from OpenGL.GL import *

class VBO:
    def __init__(self) -> None:
        self.vbo = glGenBuffers(1)
        self.component_count = 0  # Vec2, Vec3, Vec4 などの2, 3, 4
        self.vertex_count = 0

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

    def unbind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_vertex_attribute(self, component_count: int, bytelength: int,
                             data: any) -> None:
        ''' float2, 3, 4'''
        self.component_count = component_count
        stride = 4 * self.component_count
        self.vertex_count = bytelength // stride
        self.bind()
        glBufferData(GL_ARRAY_BUFFER, bytelength, data, GL_STATIC_DRAW)

    def set_slot(self, slot: int) -> None:
        self.bind()
        glEnableVertexAttribArray(slot)
        glVertexAttribPointer(slot, self.component_count, GL_FLOAT, GL_FALSE, 0, None)

    def draw(self) -> None:
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)