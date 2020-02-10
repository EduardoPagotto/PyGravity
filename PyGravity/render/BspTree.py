#!/usr/bin/env python3
'''
Created on 20200210
Update on 20200210
@author: Eduardo Pagotto
 '''

import glm
from dataclasses import dataclass 

from PyGravity.render.Triangle import Triangle

@dataclass
class BspTreeNode:
    partition : Triangle
    polygons: []
    front : any = None
    back : any = None

def bsptreeBuild(_pListPolygon) -> BspTreeNode:

    if len(_pListPolygon) == 0:
        return None

    tree = BspTreeNode(_pListPolygon.back())
    _pListPolygon.pop_back()
    tree.polygons.push_back(tree.partition)

    front_list = []
    back_list = []

    while( len(_pListPolygon) > 0 ):
        poly = _pListPolygon.back()
        _pListPolygon.pop_back()

