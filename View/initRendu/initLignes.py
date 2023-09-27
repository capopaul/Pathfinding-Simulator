# -*- coding: utf-8 -*-


#----------------------------------
from OpenGL.GL import *
import numpy as np

#----------------------------------
from View.objects.quad import *
from Usefull.fonctionsFichier import *

#----------------------------------


def initLignes(canvas):
    print("lollll", canvas.coordLigne)
    canvas.coordLigne = np.array(canvas.coordLigne.flatten(), 'f')
    vertex = np.array([],'f')
    canvas.indexLignes = np.array([], dtype=np.uint32)
    
    AlgoColor = list(map(float, config().ReturnValue('AlgoColor').split(",")))
    
    vertex, canvas.indexLignes = add_quad(vertex, canvas.indexLignes, 
                                                         [0,0.15,0], 
                                                         [1,0.15,1], 
                                                         [129/255, 41/255, 244/255])
    #VAO
    canvas.VAOLignes = glGenVertexArrays(1)
    glBindVertexArray(canvas.VAOLignes)
    
    indice_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indice_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(canvas.indexLignes)*4, canvas.indexLignes, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex)*4, vertex, GL_STATIC_DRAW)
    
    loc_positions = glGetAttribLocation(canvas.shader_Lignes, 'positions')
    glVertexAttribPointer(loc_positions, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_positions)
        
    loc_colors = glGetAttribLocation(canvas.shader_Lignes, 'inObjectColor')
    glVertexAttribPointer(loc_colors, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(4*3))
    glEnableVertexAttribArray(loc_colors)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    canvas.instance_buffer = glGenBuffers(1)
    

    glBindBuffer(GL_ARRAY_BUFFER, canvas.instance_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(canvas.coordLigne)*4, canvas.coordLigne, GL_STATIC_DRAW)
    
    
    loc_offset = glGetAttribLocation(canvas.shader_Lignes, 'Offset')
    glVertexAttribPointer(loc_offset, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_offset)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    glVertexAttribDivisor(loc_offset, 1)
    
    canvas.loc_mvp = glGetUniformLocation(canvas.shader_Lignes, "mvp")

    glBindVertexArray(0)
    
    
