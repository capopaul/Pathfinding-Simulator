# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
import numpy as np

#----------------------------------
from View.objects.quad import *
from Usefull.fonctionsFichier import *

#----------------------------------

def initAlgo(canvas):
    
    vertex = np.array([],'f')
    canvas.indexAlgo = np.array([], dtype=np.uint32)
    
    AlgoColor = list(map(float, config().ReturnValue('AlgoColor').split(",")))
    
    vertex, canvas.indexAlgo = add_quad(vertex, canvas.indexAlgo, 
                                                         [0,0.15,0], 
                                                         [1,0.15,1], 
                                                         [*AlgoColor])
    #VAO
    canvas.VAOAlgo = glGenVertexArrays(1)
    glBindVertexArray(canvas.VAOAlgo)
    
    indice_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indice_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(canvas.indexAlgo)*4, canvas.indexAlgo, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex)*4, vertex, GL_STATIC_DRAW)
    
    loc_positions = glGetAttribLocation(canvas.shader_Algo, 'positions')
    glVertexAttribPointer(loc_positions, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_positions)
        
    loc_colors = glGetAttribLocation(canvas.shader_Algo, 'inObjectColor')
    glVertexAttribPointer(loc_colors, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(4*3))
    glEnableVertexAttribArray(loc_colors)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    canvas.instance_buffer = glGenBuffers(1)
    
    arr1, arr2 = np.where(canvas.tableauMap == 0)
    canvas.sizeBuffer = 4*(2*len(arr1)+2)
    glBindBuffer(GL_ARRAY_BUFFER, canvas.instance_buffer)
    glBufferData(GL_ARRAY_BUFFER, canvas.sizeBuffer, canvas.AlgoCube, GL_DYNAMIC_DRAW)
    
    
    loc_offset = glGetAttribLocation(canvas.shader_Algo, 'Offset')
    glVertexAttribPointer(loc_offset, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_offset)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    glVertexAttribDivisor(loc_offset, 1)
    
    canvas.loc_mvp = glGetUniformLocation(canvas.shader_Algo, "mvp")

    glBindVertexArray(0)
    
    