#!/usr/bin/env python3
'''
Created on 202002204
Update on 202002204
@author: Eduardo Pagotto
'''

from OpenGL.GL import *

class IBO:
    def __init__(self) -> None:
        self.vbo = glGenBuffers(1)
        self.index_count = 0
        self.index_type = 0

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo)

    def unbind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def set_indices(self, stride: int, bytelength: int, data: Any) -> None:
        self.index_count = bytelength // stride
        self.bind()
        if stride == 1:
            self.index_type = GL_UNSIGNED_BYTE
        elif stride == 2:
            self.index_type = GL_UNSIGNED_SHORT
        elif stride == 4:
            self.index_type = GL_UNSIGNED_INT
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, bytelength, data, GL_STATIC_DRAW)

    def draw(self) -> None:
        glDrawElements(GL_TRIANGLES, self.index_count, self.index_type, None)