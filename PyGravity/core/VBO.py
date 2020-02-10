#!/usr/bin/env python3
'''
Created on 202002204
Update on 202002204
@author: Eduardo Pagotto
'''

from PyGravity.core.VertexData import VertexData, sizeOfVertexData
from OpenGL.GL import *

class VBO:
    def __init__(self) -> None:
        self.vboGL = glGenBuffers(1)
        #self.component_count = 0  # Vec2, Vec3, Vec4 などの2, 3, 4
        #self.vertex_count = 0

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.vboGL])

    def set_slot(self, slotID, slotSize, offset):
        glVertexAttribPointer(slotID, slotSize, GL_FLOAT, GL_FALSE, sizeOfVertexData(), offset)
        glEnableVertexAttribArray(slotID)
    
    def bind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.vboGL)

    def unbind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def building(self):
        # Vertex fields ids
        self.set_slot(0, 3, 0)  # Vertice
        self.set_slot(1, 3, 12) # Normal
        self.set_slot(2, 2, 24) # Texture

        # limpa dados
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        glDisableVertexAttribArray(0) # Slot 0 Vertice
        glDisableVertexAttribArray(1) # Slot 1 Normal
        glDisableVertexAttribArray(2) # Slot 2 Textura

    def buildStatic(self, vertexData):
        # Buffer de vertice
        #glGenBuffers(1, vboGL)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboGL)
        glBufferData(GL_ARRAY_BUFFER, vertexData.size() * sizeof(VertexData), vertexData[0], GL_STATIC_DRAW)
        self.building()

    def buildDynamic(self, maxBufferSize):
        # Buffer de vertice
        glBindBuffer(GL_ARRAY_BUFFER, self.vboGL)
        glBufferData(GL_ARRAY_BUFFER, maxBufferSize, None, GL_STREAM_DRAW)

        self.building()


    # def set_vertex_attribute(self, component_count: int, bytelength: int,
    #                          data: any) -> None:
    #     ''' float2, 3, 4'''
    #     self.component_count = component_count
    #     stride = 4 * self.component_count
    #     self.vertex_count = bytelength // stride
    #     self.bind()
    #     glBufferData(GL_ARRAY_BUFFER, bytelength, data, GL_STATIC_DRAW)

    # def set_slot(self, slot: int) -> None:
    #     self.bind()
    #     glEnableVertexAttribArray(slot)
    #     glVertexAttribPointer(slot, self.component_count, GL_FLOAT, GL_FALSE, 0, None)

    # def draw(self) -> None:
    #     glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)