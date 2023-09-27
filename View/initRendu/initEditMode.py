# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np
from OpenGL.GL import *

#----------------------------------
from View.objects.quad import *

#----------------------------------

def initEditMode(canvas):
    vertex = np.array([],'f')
    
    epaisseurCroix = 0.01
    
    vertex, canvas.indexEditMode = add_quad(vertex, canvas.indexEditMode, [-epaisseurCroix/2, -2*epaisseurCroix/2, 0], [epaisseurCroix/2, 2*epaisseurCroix/2, 0], [1,1,1])
    
    vertex, canvas.indexEditMode = add_quad(vertex, canvas.indexEditMode, [-2*epaisseurCroix/2, -epaisseurCroix/2, 0], [2*epaisseurCroix/2, epaisseurCroix/2, 0], [1,1,1])
    
    vertex = np.array(vertex, dtype= np.float32)
    canvas.indexEditMode = np.array(canvas.indexEditMode, dtype = np.uint32)

    canvas.VAOEditMode = glGenVertexArrays(1)
    glBindVertexArray(canvas.VAOEditMode)
    
    indice_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indice_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(canvas.indexEditMode)*4, canvas.indexEditMode, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex)*4, vertex, GL_STATIC_DRAW)
    
    loc_positions = glGetAttribLocation(canvas.shader_EditMode, 'positions')
    glVertexAttribPointer(loc_positions, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_positions)
        
    loc_colors = glGetAttribLocation(canvas.shader_EditMode, 'inObjectColor')
    glVertexAttribPointer(loc_colors, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(4*3))
    glEnableVertexAttribArray(loc_colors)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    glBindVertexArray(0)
    