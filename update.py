# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
from keyboard import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#----------------------------------
from View.Camera import *
from View.Draw.elementsBase import *
from View.Draw.AfficherMap import *
from View.Draw.Simulation import *
from Controller.eventManager import *
from View.render import *
from View.objects.cube import *
from View.initRendu.initMur import *
from View.initRendu.initObjects import *
from View.initRendu.initSimulation import *
from View.initRendu.initMarge import *
from View.initRendu.initAlgo import initAlgo
from View.initRendu.initLignes import *

#----------------------------------

"""
Boucle qui s'execute tout le temps
"""
def update(self):
    
    eventManager(self)
        
    Camera(self)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    repere(100)
    rendu = render(self)
    
    if self.actualiser:
        self.actualiser = False
        initMur(self)
        initObjects(self)
        initLignes(self)
        
        
        if self.afficherMarge:
            initMarge(self)
        self.afficherMap = True
    
    if self.afficherMap:
        rendu.Mur()
        rendu.Objects()
        rendu.Lignes()
        if self.editMode:
            rendu.EditMode()
        
        
        if self.afficherMarge:
            rendu.Marge()
    
        if self.simulation:
            simulation(self)
            if self.afficherAlgo == 0:
                initAlgo(self)
                self.afficherAlgo = 1
            elif self.afficherAlgo == 1:
                rendu.Algo()

        if self.afficherSolution == 1:
            rendu.Simulation()
        elif self.afficherSolution == 0:
            initSimulation(self)
            self.afficherSolution = 1
      
    self.SwapBuffers()