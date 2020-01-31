#!/usr/bin/env python3
'''
Created on 20191125
Update on 20191125
@author: Eduardo Pagotto
 '''

import numpy as np
from PIL import Image

from PyGravity.core.Canvas import Canvas
from PyGravity.core.FlowControl import FlowControl
from PyGravity.core.IClient import IClient

class ClientGame(IClient):
    def __init__(self, canvas):
        self.canvas = canvas

    def start(self):
        return

    def stop(self):
        return

    def render(self):
        return

    def keyCapture(self, tecla):
        return

    def mouseButtonDownCapture(self, mb):
        return

    def mouseButtonUpCapture(self, mb):
        return

    def mouseMotionCapture(self, mb):
        return

    def joystickCapture(self, joy):
        return

    def joystickStatus(self, joy):
        return

    def userEvent(self, _event):
        return

    def newFPS(self, fps):
        return

    def windowEvent(self, _event):
        return

    def paused(self):
        return False




    
if __name__ == '__main__':

    canvas = Canvas("teste", 640, 480)
    
    client = ClientGame(canvas)

    flow = FlowControl(client)
    flow.open()
    flow.loop()





    print('fim')
    # ar = np.array( [[100, 100, 100, 100],
    #                 [100, 120, 120, 100],
    #                 [100, 120, 120, 100],
    #                 [100, 100, 100, 100]], dtype=np.uint8)

    # ar = np.array( [[90, 90, 90, 90, 90, 100, 100, 100],
    #                 [100, 100, 100, 110, 110, 110, 110, 100],
    #                 [100, 100, 100, 100, 120, 120, 120, 100],
    #                 [95, 80, 70, 100, 150, 150, 150, 100],
    #                 [90, 85, 75, 105, 155, 155, 120, 100],
    #                 [100, 100, 100, 125, 150, 120, 100, 100],
    #                 [100, 105, 110, 110, 115, 120, 100, 100],
    #                 [100, 110, 115, 120, 120, 120, 125, 130]], dtype=np.uint8)

    # ar = np.array( [[100, 100, 120, 120, 120, 120, 150, 200, 200, 200, 120, 120, 120, 120, 130, 150],
    #                 [100, 100, 100, 100, 120, 120, 150, 150, 200, 120, 120, 120, 120, 80 , 130, 150],
    #                 [100, 100, 100, 100, 100, 120, 150, 150, 150, 120, 120, 120, 100, 80 , 130, 150],
    #                 [100, 100, 100, 100, 100, 100, 120, 150, 150, 120, 120, 100, 100, 80 , 130, 150],
    #                 [100, 100, 100, 100, 100, 100, 120, 120, 100, 100, 100, 100, 80 , 80 , 100, 130],
    #                 [100, 100, 100, 95 , 95 , 120, 120, 120, 100, 50 , 20 , 100, 80 , 80 , 100, 100],
    #                 [100, 100, 95 , 80 , 80 , 95 , 70 , 60 , 40 , 20 , 20 , 40 , 80 , 80 , 95 , 100],
    #                 [90 , 95 , 80 , 80 , 70 , 70 , 70 , 60 , 40 , 20 , 40 , 40 , 80 , 100, 95 , 95 ],
    #                 [90 , 95 , 80 , 70 , 70 , 90 , 90 , 100, 100, 50 , 50 , 100, 80 , 100, 100, 95 ],
    #                 [90 , 95 , 95 , 80 , 70 , 100, 120, 120, 120, 100, 100, 100, 80 , 80 , 100, 95 ],
    #                 [90 , 100, 95 , 95 , 95 , 120, 120, 120, 120, 120, 100, 100, 80 , 80 , 100, 95 ],
    #                 [90 , 100, 100, 100, 120, 120, 120, 150, 150, 120, 120, 100, 80 , 80 , 95 , 95 ],
    #                 [90 , 100, 100, 120, 120, 120, 120, 150, 150, 120, 120, 100, 80 , 80 , 95 , 95 ],
    #                 [90 , 90 , 100, 100, 120, 120, 150, 200, 200, 150, 120, 100, 80 , 80 , 100, 100],
    #                 [90 , 90 , 100, 100, 120, 150, 150, 250, 250, 200, 150, 120, 100, 80 , 100, 150],
    #                 [90 , 90 , 120, 120, 120, 150, 250, 250, 250, 250, 150, 120, 100, 100, 150, 200]], dtype=np.uint8)



    #ar = np.ones((512,512), dtype=np.uint16)
    #ar = np.full((4,4), 0,dtype=np.uint8)
    #print(str(ar))

    #im = Image.fromarray(ar)
    #im.save('heightmap_4x4.png')
    #im.save('heightmap_8x8.png')
    #im.save('heightmap_16x16.png')
