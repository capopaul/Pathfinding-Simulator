# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
import numpy as np

#----------------------------------
from View.objects.cube import *
from Usefull.fonctionsFichier import *

#----------------------------------

def initMarge(canvas):
    ySize = int(config().ReturnValue("HauteurMur"))/2
    MurColor = list(map(float, config().ReturnValue('MargeColor').split(",")))
    
    #VAO
    canvas.VAOMarge = glGenVertexArrays(1)
    glBindVertexArray(canvas.VAOMarge)
    
    vertex = arrayVertCube(pos1=(0,0,0), pos2=(1, ySize, 1), color=[*MurColor])
    canvas.indexMarge = arrayIndexCube(0)
    
    indice_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indice_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(canvas.indexMarge)*4, canvas.indexMarge, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex)*4, vertex, GL_STATIC_DRAW)
    
    loc_positions = glGetAttribLocation(canvas.shader_Marge, 'positions')
    glVertexAttribPointer(loc_positions, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_positions)
        
    loc_colors = glGetAttribLocation(canvas.shader_Marge, 'inObjectColor')
    glVertexAttribPointer(loc_colors, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(4*3))
    glEnableVertexAttribArray(loc_colors)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    instance_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, instance_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(canvas.Marge)*4, canvas.Marge, GL_STATIC_DRAW)
    
    loc_offset = glGetAttribLocation(canvas.shader_Marge, 'Offset')
    glVertexAttribPointer(loc_offset, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_offset)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    glVertexAttribDivisor(loc_offset, 1)
    
    canvas.loc_mvp = glGetUniformLocation(canvas.shader_Marge, "mvp")
    
    glBindVertexArray(0)