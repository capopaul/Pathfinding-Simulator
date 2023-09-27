# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
import pyrr
import numpy as np
#----------------------------------s
from View.shaders.ShaderLoader import *
#----------------------------------s

class render:
    def __init__(self, canvas):
        proj_matrix = pyrr.matrix44.create_perspective_projection_matrix(70.0, canvas.GetSize()[0]/canvas.GetSize()[1], 0.1, 1000.0)
        view_matrix = pyrr.matrix44.create_look_at(canvas.cameraPosition, canvas.cameraPointCible, canvas.axeVertical)
        
        self.transform = pyrr.matrix44.multiply(view_matrix, proj_matrix)
        self.canvas = canvas
         
    def Mur(self):
        glUseProgram(self.canvas.shader_Wall)
        glBindVertexArray(self.canvas.VAOMur)
        glUniformMatrix4fv(self.canvas.loc_mvp, 1, GL_FALSE, self.transform)
        glDrawElementsInstanced(GL_TRIANGLES, len(self.canvas.indexMur), GL_UNSIGNED_INT, None, int(len(self.canvas.Mur)/2))
        glUseProgram(0)
        
     
    def Marge(self):
        glUseProgram(self.canvas.shader_Marge)
        glBindVertexArray(self.canvas.VAOMarge)
        glUniformMatrix4fv(self.canvas.loc_mvp, 1, GL_FALSE, self.transform)
        glDrawElementsInstanced(GL_TRIANGLES, len(self.canvas.indexMarge), GL_UNSIGNED_INT, None, int(len(self.canvas.Marge)/2))
        glUseProgram(0)   
    
    
    def Lignes(self):
        glUseProgram(self.canvas.shader_Lignes)
        glBindVertexArray(self.canvas.VAOLignes)
        glUniformMatrix4fv(self.canvas.loc_mvp, 1, GL_FALSE, self.transform)
        glDrawElementsInstanced(GL_TRIANGLES, len(self.canvas.indexLignes), GL_UNSIGNED_INT, None, int(len(self.canvas.coordLigne)/2))
        glUseProgram(0)
    
    def Objects(self):
        glUseProgram(self.canvas.shader_Objects)
        glBindVertexArray(self.canvas.VAOObjects)
        glUniformMatrix4fv(self.canvas.loc_mvp, 1, GL_FALSE, self.transform)
        glDrawElements(GL_TRIANGLES, len(self.canvas.indexObjects), GL_UNSIGNED_INT, None)
        glUseProgram(0)
    
    def Simulation(self):
        glUseProgram(self.canvas.shader_Simulation)
        glBindVertexArray(self.canvas.VAOSimulation)
        glUniformMatrix4fv(self.canvas.loc_mvp, 1, GL_FALSE, self.transform)
        glDrawElementsInstanced(GL_TRIANGLES, len(self.canvas.indexSimulation), GL_UNSIGNED_INT, None, int(len(self.canvas.matSimulation)/16))
        glUseProgram(0)
    
    def EditMode(self):
        glUseProgram(self.canvas.shader_EditMode)
        glBindVertexArray(self.canvas.VAOEditMode)
        glDrawElements(GL_TRIANGLES, len(self.canvas.indexEditMode), GL_UNSIGNED_INT, None)
        glUseProgram(0)
    
    def Algo(self):
        if len(self.canvas.AlgoCubeNewValue) != 0:
            glBindBuffer(GL_ARRAY_BUFFER, self.canvas.instance_buffer)
            self.canvas.nextAlgoCube = False
            
            vbo_pointer = ctypes.cast(glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY),ctypes.POINTER(ctypes.c_ubyte))
            vbo_array = np.ctypeslib.as_array(vbo_pointer,(self.canvas.sizeBuffer,))


            vbo_array[4*len(self.canvas.AlgoCube):4*len(self.canvas.AlgoCube)+(4*len(self.canvas.AlgoCubeNewValue))] = self.canvas.AlgoCubeNewValue.view(dtype='uint8').ravel()
            
            glUnmapBuffer(GL_ARRAY_BUFFER)
            
            self.canvas.AlgoCube = np.array(np.append(self.canvas.AlgoCube, self.canvas.AlgoCubeNewValue), np.float32).flatten()
            self.canvas.AlgoCubeNewValue = np.array([],'f')
            self.canvas.nextAlgoCube = True
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            
            
            
        glUseProgram(self.canvas.shader_Algo)
        glBindVertexArray(self.canvas.VAOAlgo)
        glUniformMatrix4fv(self.canvas.loc_mvp, 1, GL_FALSE, self.transform)
        glDrawElementsInstanced(GL_TRIANGLES, len(self.canvas.indexAlgo), GL_UNSIGNED_INT, None, int(len(self.canvas.AlgoCube)/2))
        glUseProgram(0)
        
    
        
        
        
        
        
        
        