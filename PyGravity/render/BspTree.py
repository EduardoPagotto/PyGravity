#!/usr/bin/env python3
'''
Created on 20200210
Update on 20200210
@author: Eduardo Pagotto
 '''

import math
import glm
from enum import Enum
from dataclasses import dataclass 

from PyGravity.render.Triangle import Triangle

EPSILON=1e-3

class SIDE(Enum):
    CP_ONPLANE = 0,
    CP_FRONT = 1,
    CP_BACK = 2, 
    CP_SPANNING = 3

@dataclass
class BspTreeNode:
    partition : Triangle
    polygons: []
    front : any = None
    back : any = None

def swapFace(a, b):
    c = b
    b = a
    a = c

def retTex1(_p0 : glm.vec2, _p1: glm.vec2) -> glm.vec2 :
    return glm.vec2(_p1.x if _p0.x < _p1.x else _p0.x, _p1.y if _p0.y < _p1.y else  _p0.y)

def retTex2(_p0 : glm.vec2, _p1: glm.vec2) -> glm.vec2 :
    # FIXME: horrivel
    dx = _p1.x - _p0.x
    dy = _p1.y - _p0.y

    vx = 0.0
    vy = 0.0

    if dx < 0:
        vx = _p1.x
    else:
        vx = _p0.x

    if dy < 0:
        vy = _p1.y
    else:
        vy = _p0.y

    return glm.vec2(vx, vy)
    # return glm::vec2((_p0.x < _p1.x) ? _p1.x : _p0.x, (_p0.y < _p1.y) ? _p1.y : _p0.y);

def aprox(dado: glm.vec3) -> glm.vec3:
    return glm.vec3(0.0 if math.fabs(dado.x) < EPSILON else dado.x, 
                    0.0 if math.fabs(dado.y) < EPSILON else dado.y,
                    0.0 if math.fabs(dado.z) < EPSILON else dado.z)

def intersect(n : glm.vec3, p0: glm.vec3, a: glm.vec3, c: glm.vec3) -> glm.vec3:
    num = glm.dot(n, a)
    cma = c - a
    denom = glm.dot(n, cma)
    D = -glm.dot(n, p0) # direção inversa
    t = -(num + D) / denom

    valor = a + t * (c - a)
    return aprox(valor)

def splitTriangle(fx: glm.vec3, _pTriangle: Triangle, _partition: Triangle , _pListPolygon: list):
    a = _pTriangle.vertex[0].position
    b = _pTriangle.vertex[1].position
    c = _pTriangle.vertex[2].position

    # acerto para vertex do tex final igualar a rotacao do triangulo
    pVertex_a = None
    pVertex_b = None
    pVertex_c = None

    # Normaliza Triangulo para que o corte do hiper-plano esteja nos segmentos de reta CA e CB (corte em a e b)
    if fx.x * fx.z >= 0: # corte em a e c
        swapFace(b, c)
        swapFace(a, b)
        pVertex_a = _pTriangle.vertex[2] # old c
        pVertex_b = _pTriangle.vertex[0] # old a
        pVertex_c = _pTriangle.vertex[1] # old b
    elif fx.y * fx.z >= 0: # corte em b e c
        swapFace(a, c)
        swapFace(a, b)
        ##--
        pVertex_a = _pTriangle.vertex[1] # old b
        pVertex_b = _pTriangle.vertex[2] # old c
        pVertex_c = _pTriangle.vertex[0] # old a
    else: # Cortre em a e b
        pVertex_a = _pTriangle.vertex[0] # old a
        pVertex_b = _pTriangle.vertex[1] # old b
        pVertex_c = _pTriangle.vertex[2] # old c
    
    # Testar ideia
    # Na textura se Xb - Xa > 0 entao Xb e [1,n] do contrario [0,n] para segmento de reta ab
    # Na textura se Yb - Ya > 0 entao Yb e [n,1] do contrario [n,0] para segmento de reta ab

    A = intersect(_partition.normal(), _partition.vertex[0].position, a, c)
    B = intersect(_partition.normal(), _partition.vertex[0].position, b, c)

    propAC = (glm.distance(A, a) / glm.distance(a, c)) # razao da distancia entre a e A
    InterTexA = propAC * pVertex_a.texture.x

    T1 = Triangle(a, b, A)
    T1.vertex[0].texture = retTex1(pVertex_c.texture, pVertex_a.texture)
    T1.vertex[1].texture = retTex1(pVertex_a.texture, pVertex_b.texture)
    T1.vertex[2].texture = glm.vec2(InterTexA, pVertex_a.texture.y) # A

    #--

    T2 = Triangle(b, B, A)
    T2.vertex[0].texture = retTex1(pVertex_a.texture, pVertex_b.texture) # pVertex_b->texture; # b old c
    # T2.vertex[0].texture = retTex1(pVertex_c->texture, pVertex_b->texture);

    # Hipotenusa e cateto oposto para pegar o seno rad1
    hypo = glm.distance(c, b)  # segmento de reta de c' ate b'
    catOp = glm.distance(a, b) # segmento a' ate b'
    rad1 = catOp / hypo

    # Hipotenusa e seno para calcular o valor do cateto opposo (proporcao x da textura)
    hypo2 = glm.distance(c, B)
    seno1 = rad1
    val_final = seno1 * hypo2         # valor da imagem do ponto B em Y (cateto oposto)
    valxTexTemp = glm.distance(a, b) # tamanho total do Y
    valxTex = val_final / valxTexTemp # razao da textura em X ufa!!!

    T2.vertex[1].texture = glm.vec2(InterTexA, valxTex)             # B
    T2.vertex[2].texture = glm.vec2(InterTexA, pVertex_a.texture.y) # A

    # --

    T3 = Triangle(A, B, c)
    T3.vertex[0].texture = glm.vec2(InterTexA, pVertex_a.texture.y)      # A
    T3.vertex[1].texture = glm.vec2(InterTexA, valxTex)                  # B
    T3.vertex[2].texture = retTex2(pVertex_b.texture, pVertex_c.texture) # c old a

    for i in range(3):
        T1.vertex[i].normal = _pTriangle.vertex[i].normal
        T2.vertex[i].normal = _pTriangle.vertex[i].normal
        T3.vertex[i].normal = _pTriangle.vertex[i].normal
    
    _pListPolygon.insert(0, T1)
    _pListPolygon.insert(0, T2)
    _pListPolygon.insert(0, T3)

def classifyPoly(plane: Triangle, poly: Triangle, _resultTest: glm.vec3) -> SIDE:

    infront = 0
    behind = 0
    onPlane = 0
    result = [0.0 for _ in range(3)] #result[3] = 0

    for a in range(3):

        direction = plane.vertex[0].position - poly.vertex[a].position
        result[a] = glm.dot(direction, plane.normal())
        if result[a] > EPSILON:
            behind += 1
        elif result[a] < -EPSILON: 
            infront += 1
        else:
            onPlane += 1
            infront += 1
            behind += 1
        
    _resultTest.x = result[0]
    _resultTest.y = result[1]
    _resultTest.z = result[2]

    if onPlane == 3:
        return SIDE.CP_ONPLANE

    if behind == 3:
        return SIDE.CP_BACK

    if infront == 3:
        return SIDE.CP_FRONT

    return SIDE.CP_SPANNING

def bsptreeBuild(_pListPolygon) -> BspTreeNode:

    if len(_pListPolygon) == 0:
        return None

    tree = BspTreeNode(_pListPolygon.pop()) # remove do final
    tree.polygons.insert(0, tree.partition) # insere no inicio

    front_list = []
    back_list = []

    while( len(_pListPolygon) > 0 ):
        poly = _pListPolygon.pop()

        result = glm.vec3(0.0)
        
        teste = classifyPoly(tree.partition, poly, result)

        if (teste == SIDE.CP_BACK):
            back_list.insert(0, poly) #push_back(poly)
        elif (teste == SIDE.CP_FRONT):
            front_list.insert(0, poly) #.push_back(poly)
        elif (teste == SIDE.CP_ONPLANE):
            tree.polygons.push_back(poly)
        else: # CP_SPANNING
            splitTriangle(result, poly, tree.partition, _pListPolygon)

    tree.front = bsptreeBuild(front_list)
    tree.back = bsptreeBuild(back_list)

    return tree