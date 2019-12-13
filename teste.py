#!/usr/bin/env python3
'''
Created on 20191125
Update on 20191125
@author: Eduardo Pagotto
 '''

import numpy as np
from PIL import Image


if __name__ == '__main__':

    ar = np.array( [[90, 90, 90, 90, 90, 100, 100, 100],
                    [100, 100, 100, 110, 110, 110, 110, 100],
                    [100, 100, 100, 100, 120, 120, 120, 100],
                    [95, 80, 70, 100, 150, 150, 150, 100],
                    [90, 85, 75, 105, 155, 155, 120, 100],
                    [100, 100, 100, 125, 150, 120, 100, 100],
                    [100, 105, 110, 110, 115, 120, 100, 100],
                    [100, 110, 115, 120, 120, 120, 125, 130]], dtype=np.uint8)

    #ar = np.ones((512,512), dtype=np.uint16)
    #ar = np.full((4,4), 0,dtype=np.uint8)
    print(str(ar))

    im = Image.fromarray(ar)
    im.save('heightmap_8x8.png')
