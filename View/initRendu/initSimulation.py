# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
import numpy as np
import pyrr
#----------------------------------
from View.objects.cube import *
from Usefull.fonctionsFichier import *
from Model.usefull import angleVecteur, normeVecteur
#----------------------------------

    
def initSimulation(canvas):
    vertex = np.array([],'f')
    canvas.indexSimulation = np.array([], dtype=np.uint32)
    
    SolutionColor = list(map(float, config().ReturnValue('SolutionColor').split(",")))
    
    vertex = arrayVertCube(pos1=(0,0,0), pos2=(1, 0.2, 0.2), color=[*SolutionColor])
    canvas.indexSimulation = arrayIndexCube(0)
    for index in range(len(canvas.vecteurSolution)):
        vecteur_translantion = pyrr.Vector3([canvas.pointSolution[index,0]+0.6,0.3,canvas.pointSolution[index,1]+0.6])
        translate_matrix = pyrr.matrix44.create_from_translation(vecteur_translantion)
        
        
        result = angleVecteur(canvas.vecteurSolution[index])
        scale_matrix = pyrr.matrix44.create_from_scale([normeVecteur(canvas.vecteurSolution[index]),1,1])
        
        rotation_matrix = pyrr.Matrix44.from_y_rotation(result)
        
        transform_matrix = pyrr.matrix44.multiply(scale_matrix, rotation_matrix)
        transform_matrix = pyrr.matrix44.multiply(transform_matrix, translate_matrix)
        canvas.matSimulation = np.append(canvas.matSimulation, transform_matrix)    
    

    canvas.matSimulation = np.array(canvas.matSimulation, np.float32).flatten()
    
    canvas.VAOSimulation = glGenVertexArrays(1)
    glBindVertexArray(canvas.VAOSimulation)
    
    indice_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indice_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(canvas.indexSimulation)*4, canvas.indexSimulation, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex)*4, vertex, GL_DYNAMIC_DRAW)
    
    loc_positions = glGetAttribLocation(canvas.shader_Simulation, 'positions')
    glVertexAttribPointer(loc_positions, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(loc_positions)
        
    loc_colors = glGetAttribLocation(canvas.shader_Simulation, 'inObjectColor')
    glVertexAttribPointer(loc_colors, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 6, ctypes.c_void_p(4*3))
    glEnableVertexAttribArray(loc_colors)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    

    instance_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, instance_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(canvas.matSimulation)*4, canvas.matSimulation, GL_STATIC_DRAW)
    
    loc_transform = glGetAttribLocation(canvas.shader_Simulation, 'transform')
    
    glEnableVertexAttribArray(loc_transform); 
    glVertexAttribPointer(loc_transform, 4, GL_FLOAT, GL_FALSE, 4*16, ctypes.c_void_p(0));
    glEnableVertexAttribArray(loc_transform + 1); 
    glVertexAttribPointer(loc_transform + 1, 4, GL_FLOAT, GL_FALSE, 4*16, ctypes.c_void_p(16));
    glEnableVertexAttribArray(loc_transform + 2); 
    glVertexAttribPointer(loc_transform + 2, 4, GL_FLOAT, GL_FALSE, 4*16, ctypes.c_void_p(2*16));
    glEnableVertexAttribArray(loc_transform + 3); 
    glVertexAttribPointer(loc_transform + 3, 4, GL_FLOAT, GL_FALSE, 4*16, ctypes.c_void_p(3*16));

    glVertexAttribDivisor(loc_transform, 1);
    glVertexAttribDivisor(loc_transform + 1, 1);
    glVertexAttribDivisor(loc_transform + 2, 1);
    glVertexAttribDivisor(loc_transform + 3, 1);

    glVertexAttribDivisor(loc_transform, 1)
    
    canvas.loc_mvp = glGetUniformLocation(canvas.shader_Simulation, "mvp")
    
    glBindVertexArray(0)
    
    
    
    