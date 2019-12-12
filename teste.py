#!/usr/bin/env python3
'''
Created on 20191125
Update on 20191125
@author: Eduardo Pagotto
 '''

import numpy as np
from PIL import Image


if __name__ == '__main__':

    ar = np.array( [[128, 128, 128, 128],
                    [128, 255, 255, 128],
                    [128,  80,   0, 128],
                    [128, 128, 128, 128]], dtype=np.uint8)

    #ar = np.ones((512,512), dtype=np.uint16)
    #ar = np.full((4,4), 0,dtype=np.uint8)
    print(str(ar))

    im = Image.fromarray(ar)
    im.save('heightmap1.tga')
