# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np
#----------------------------------

#----------------------------------

def arrayVertCube(pos1, pos2, color):
    Color = np.array(color,'f')
    return np.array([
        pos1[0] ,pos1[1], pos1[2], *Color,  pos1[0] ,pos1[1], pos1[2], *(0.6*Color),  pos1[0] ,pos1[1], pos1[2], *(0.2*Color),
        pos2[0], pos1[1], pos1[2], *Color,  pos2[0], pos1[1], pos1[2], *(0.6*Color),  pos2[0], pos1[1], pos1[2], *(0.2*Color),
        pos1[0], pos1[1], pos2[2], *Color,  pos1[0], pos1[1], pos2[2], *(0.6*Color),  pos1[0], pos1[1], pos2[2], *(0.2*Color),
        pos2[0], pos1[1], pos2[2], *Color,  pos2[0], pos1[1], pos2[2], *(0.6*Color),  pos2[0], pos1[1], pos2[2], *(0.2*Color),      
        pos1[0], pos2[1], pos1[2], *Color,  pos1[0], pos2[1], pos1[2], *(0.6*Color),  pos1[0], pos2[1], pos1[2], *(0.2*Color),
        pos2[0], pos2[1], pos1[2], *Color,  pos2[0], pos2[1], pos1[2], *(0.6*Color),  pos2[0], pos2[1], pos1[2], *(0.2*Color),
        pos1[0], pos2[1], pos2[2], *Color,  pos1[0], pos2[1], pos2[2], *(0.6*Color),  pos1[0], pos2[1], pos2[2], *(0.2*Color),
        pos2[0], pos2[1], pos2[2], *Color,  pos2[0], pos2[1], pos2[2], *(0.6*Color),  pos2[0], pos2[1], pos2[2], *(0.2*Color),
        ],'f')

def arrayIndexCube(indexZero):
    return np.array([0,3,9,
                       0,9,6,
                       12,15,18,
                       15,18,21,
                       
                       7,10,22,
                       7,22,19,
                       1,4,16,
                       1,16,13,
                       
                       2,8,20,
                       2,14,20,
                       5,11,23,
                       5,17,23
                       ]+np.array([indexZero]*12*3), dtype=np.uint32)

def add_cube(vertex, index, instance, pos1, pos2, color):
    color = np.array(color, 'f')
    newVertex = np.concatenate((vertex, arrayVertCube(pos1, pos2, color)))
    newIndex = np.concatenate((index, arrayIndexCube(len(instance*8))))
    newInstance = np.concatenate((instance, [pos1[0] ,pos1[2]]))
    
    return newVertex, newIndex, newInstance
    
    