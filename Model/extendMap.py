# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np

#----------------------------------
from Usefull.fonctionsFichier import *
from View.Draw.AfficherMap import *
from Model.usefull import *
#----------------------------------

def ExtendMap(canvas):
    _extensionX = int(config().LargeurMur)
    _extensionZ = int(config().LongueurMur)
    
    newMap = canvas.tableauMap

    newMap[canvas.coordStartRobot[1],canvas.coordStartRobot[0]] = 0
    newMap[canvas.coordEndRobot[1],canvas.coordEndRobot[0]] = 0

    H, W, N, M = len(canvas.tableauMap), len(canvas.tableauMap[0]), int(config().LargeurMur), int(config().LongueurMur)
    newMap = np.repeat(canvas.tableauMap, M).reshape(H, M*W)
    newMap = np.repeat(newMap, N, axis=0).reshape(N*H, M*W)
    
    newMap[canvas.coordStartRobot[1]*M+int(M/2),canvas.coordStartRobot[0]*N+int(N/2)] = 4    
    newMap[canvas.coordEndRobot[1]*M+int(M/2),canvas.coordEndRobot[0]*N+int(N/2)] = 5    

    canvas.tableauMap = newMap
    
    coordStartRobot(canvas,[canvas.coordStartRobot[0]*N+int(N/2), canvas.coordStartRobot[1]*M+int(M/2)])  
    coordEndRobot(canvas, [canvas.coordEndRobot[0]*N+int(N/2), canvas.coordEndRobot[1]*M+int(M/2)] )
    
    afficher_map(canvas)
    
    