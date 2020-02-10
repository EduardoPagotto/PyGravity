#!/usr/bin/env python3
'''
Created on 202002210
Update on 202002210
@author: Eduardo Pagotto
'''

import glm
from dataclasses import dataclass 

@dataclass
class VertexData:
    position : glm.vec3  # 3 * 4 = 12 ( 0 - 11)
    normal : glm.vec3    # 3 * 4 = 12 (12 - 23)
    texture : glm.vec2   # 2 * 4 = 08 (24 - 31)
    
def sizeOfVertexData() -> int:
    return (2 * glm.sizeof(glm.vec3)) + glm.sizeof(glm.vec2) 
