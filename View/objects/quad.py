# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np
#----------------------------------

#----------------------------------



def arrayVertQuad(pos1, pos2, color):
    Color = np.array(color,'f')
    return np.array([
        pos1[0] ,pos1[1], pos1[2], *Color,
        pos2[0] ,pos1[1], pos1[2], *Color,
        
        pos1[0] ,pos2[1], pos2[2], *Color,
        pos2[0] ,pos2[1], pos2[2], *Color
        ],'f')

def arrayIndexQuad(indexZero):
    return np.array([0,1,2,
                     1,2,3
                     ]+np.array([indexZero]), dtype=np.uint32)

def add_quad(vertex, index, pos1, pos2, color):
    color = np.array(color, 'f')
    newIndex = np.concatenate((index, arrayIndexQuad(len(vertex)/6)))
    newVertex = np.concatenate((vertex, arrayVertQuad(pos1, pos2, color)))
    
    
    return newVertex, newIndex
    