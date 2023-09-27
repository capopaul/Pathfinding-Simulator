# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
import numpy as np

#----------------------------------
from View.Draw.elementsBase import *
from View.objects.quad import *
#----------------------------------

def initObjects(canvas):
    canvas.vertexObjects = np.array([],'f')
    canvas.indexObjects = np.array([], dtype=np.uint32)
    
    wall(canvas, canvas.tableauMap.shape[1], canvas.tableauMap.shape[0])
    #Sol
    canvas.vertexObjects, canvas.indexObjects = add_quad(canvas.vertexObjects, canvas.indexObjects, 
                                                         [-1,-0.001,-1], 
                                                         [canvas.tableauMap.shape[1]+1,-0.001,canvas.tableauMap.shape[0]+1], 
                                                         [0,0,0])
    #Case de départ
    canvas.vertexObjects, canvas.indexObjects = add_quad(canvas.vertexObjects, canvas.indexObjects, 
                                                         np.insert(np.array(np.column_stack((np.flip(np.where(canvas.tableauMap == 4)))),'f'), 1, 0.2), 
                                                         np.insert(np.array(np.column_stack((np.flip(np.where(canvas.tableauMap == 4)))),'f'), 1, 0.2)+[1,0,1], 
                                                         [0,1,0])
    #Case d'arrivé
    
    canvas.vertexObjects, canvas.indexObjects = add_quad(canvas.vertexObjects, canvas.indexObjects, 
                                                         np.insert(np.array(np.column_stack((np.flip(np.where(canvas.tableauMap == 5)))),'f'), 1, 0.3), 
                                                         np.insert(np.array(np.column_stack((np.flip(np.where(canvas.tableauMap == 5)))),'f'), 1, 0.3)+[1,0,1], 
                                                         [1,0.5,0])
    canvas.VAOObjects = glGenVertexArrays(1)
    glBindVertexArray(canvas.VAOObjects)
    
    indice_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indice_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(canvas.indexObjects)*4, canvas.indexObjects, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(canvas.vertexObjects)*4, canvas.vertexObjects, GL_DYNAMIC_DRAW)
    
    loc_positions = glGetAttribLocation(canvas.shader_Objects, 'positions')
    glVertexAttribPointer(loc_positions, 3, GL_FLOAT, GL_FALSE, canvas.vertexObjects.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_positions)
        
    loc_colors = glGetAttribLocation(canvas.shader_Objects, 'inObjectColor')
    glVertexAttribPointer(loc_colors, 3, GL_FLOAT, GL_FALSE, canvas.vertexObjects.itemsize * 6, ctypes.c_void_p(4*3))
    glEnableVertexAttribArray(loc_colors)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    canvas.loc_mvp = glGetUniformLocation(canvas.shader_Objects, "mvp")
    
    glBindVertexArray(0)
    
    