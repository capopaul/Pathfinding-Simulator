# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np

#----------------------------------
from View.Draw.AfficherMap import *

#----------------------------------

def Marges(canvas):
    
    _nouvelleMap = np.copy(canvas.tableauMap)
    
    
    #Liste des Murs ou des Marges
    listeM = np.array(np.column_stack((np.where(canvas.tableauMap == 2))))
    if listeM.size == 0:
        listeM = np.array(np.column_stack((np.where(canvas.tableauMap == 1))))

    _extremite = np.array([[1, 0], [-1, 0],
                         [0, 1], [0, -1],
                         [1, 1], [-1, -1],
                         [1, -1], [-1, 1]])
    for m in listeM:
        for edit in _extremite:
            sell = m+edit
            if (sell[0] >= 0 and sell[0] < canvas.tableauMap.shape[0] and 
                sell[1] >=0 and sell[1] < canvas.tableauMap.shape[1]):
                if canvas.tableauMap[sell[0],sell[1]] == 0:
                    _nouvelleMap[sell[0],sell[1]] = 2
   
    
    for _x in range(canvas.tableauMap.shape[1]):
        if _nouvelleMap[0][_x] == 0:
            _nouvelleMap[0][_x] = 2
        if _nouvelleMap[canvas.tableauMap.shape[0]-1][_x] == 0:
            _nouvelleMap[canvas.tableauMap.shape[0]-1][_x] = 2
    
    for _z in range(1, canvas.tableauMap.shape[0]-1):
        if _nouvelleMap[_z][0] == 0:
            _nouvelleMap[_z][0] = 2
        if _nouvelleMap[_z][canvas.tableauMap.shape[1]-1] == 0:
            _nouvelleMap[_z][canvas.tableauMap.shape[1]-1] = 2
            
                        
    canvas.tableauMap = _nouvelleMap
    canvas.afficherMarge = True
    afficher_map(canvas)
    
    
    
    
    
def ResetMarges(canvas):
    canvas.afficherMarge = False
    for i in range(0, len(canvas.Marge),2):
        canvas.tableauMap[int(canvas.Marge[i+1]), int(canvas.Marge[i])] = 0
    canvas.Marge = np.array([])