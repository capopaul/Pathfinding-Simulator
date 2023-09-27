# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np

#----------------------------------
from Usefull.fonctionsFichier import *
from View.Draw.AfficherMap import *
from Model.usefull import *
#----------------------------------


def ExtendLab(canvas):
    print("J'aime les licornes !")
    
    largeurMur = int(config().LargeurMur)
    LargeurCase = int(config().LargeurCase)
    LongueurCase = int(config().LongueurCase)
    
    newMap = canvas.tableauMap

    newMap[canvas.coordStartRobot[1],canvas.coordStartRobot[0]] = 0
    newMap[canvas.coordEndRobot[1],canvas.coordEndRobot[0]] = 0
    
    #Ajout de la colonne fictive et de la ligne fictive pour que le tableau soit pair ( ajout de la ligne ; puis de la colonne)
    newMap = np.concatenate((newMap, np.ones((1,newMap.shape[1]))))
    newMap = np.concatenate((newMap, np.ones((newMap.shape[0],1))),1)
    """
    initSize = (nombreLigne = nombre de cube de large en X = longueur d'une colonne ,,,,, nombreColomne = nombre de cube de large en Z = longueur d'une ligne)
     
    nbCase = (nbCaseX, nbCaseZ)

    """
    initSize = np.array(newMap.shape)
    nbCase = np.array((initSize/2), dtype=uint32)
    
    #Largeur des murs
    newMap = newMap.reshape(2*nbCase[0]*nbCase[1],2)
    
    toAdd= np.array([newMap[:,-1]]).T
    for _ in range(largeurMur-1):
        newMap = np.concatenate((newMap, toAdd), axis=1)
    newMap = newMap.reshape(initSize[0], initSize[1]+int(nbCase[1])*(largeurMur-1))
    
    
    
    #Supression des colonnes fictives qui etaient à la fin
    for _ in range(largeurMur):
        newMap = np.delete(newMap, -1, axis=1)
    
    
    #Ajout de la colonne fictive au debut
    for _ in range(largeurMur):
        newMap = np.insert(newMap, 0, 1 , axis=1)
    
    
    #Largeur des cases
    initSize = np.array(newMap.shape)
    newMap = newMap.reshape(2*nbCase[0]*nbCase[1],1+largeurMur)
    
    toAdd= np.array([newMap[:,-1]]).T
    for _ in range(LargeurCase-1):
        newMap = np.concatenate((newMap, toAdd), axis=1)
    newMap = newMap.reshape(initSize[0], initSize[1]+int(nbCase[1])*(LargeurCase-1))
    
    #Supression des colonnes fictives qui etaient au debut
    for _ in range(largeurMur):
        newMap = np.delete(newMap, 0, axis=1)
    newMap = np.delete(newMap, -1, axis=0)

    #---------------------------------------------------------------------------------------------------------------------
    #On transpose pour effectuer les modifications dans l'autre sens
    newMap = newMap.T
    nbCase = nbCase[::-1]
    
    newMap = np.concatenate((newMap, np.ones((1,newMap.shape[1]))))
    newMap = np.concatenate((newMap, np.ones((newMap.shape[0],1))),1)
    initSize = np.array(newMap.shape)
    
    print(newMap, newMap.shape, nbCase)
    #Largeur des murs
    newMap = newMap.reshape(initSize[0]*nbCase[1],2)
    
    toAdd= np.array([newMap[:,-1]]).T
    for _ in range(largeurMur-1):
        newMap = np.concatenate((newMap, toAdd), axis=1)
    newMap = newMap.reshape(initSize[0], initSize[1]+int(nbCase[1])*(largeurMur-1))
    
    print(newMap)
    
    #Supression des colonnes fictives qui etaient à la fin
    for _ in range(largeurMur):
        newMap = np.delete(newMap, -1, axis=1)
    
    #Ajout de la colonne fictive au debut
    for _ in range(largeurMur):
        newMap = np.insert(newMap, 0, 1 , axis=1)
    
    
    #Largeur des cases
    initSize = np.array(newMap.shape)
    newMap = newMap.reshape(initSize[0]*nbCase[1],1+largeurMur)
    
    toAdd= np.array([newMap[:,-1]]).T
    for _ in range(LongueurCase-1):
        newMap = np.concatenate((newMap, toAdd), axis=1)
    newMap = newMap.reshape(initSize[0], initSize[1]+int(nbCase[1])*(LongueurCase-1))
    
    #Supression des colonnes fictives qui etaient au debut
    for _ in range(largeurMur):
        newMap = np.delete(newMap, 0, axis=1)
    newMap = np.delete(newMap, -1, axis=0)
    
    print(newMap)
    
    #On retranspose pour remettre comme avant
    newMap = newMap.T
    nbCase = nbCase[::-1]
    
    
    
    canvas.tableauMap = newMap
    newMap[int(canvas.coordStartRobot[1]/2)*(largeurMur+LongueurCase)+int(LongueurCase/2),int(canvas.coordStartRobot[0]/2)*(largeurMur+LargeurCase)+int(LargeurCase/2)] = 4
    newMap[int(canvas.coordEndRobot[1]/2)*(largeurMur+LongueurCase)+int(LongueurCase/2),int(canvas.coordEndRobot[0]/2)*(largeurMur+LargeurCase)+int(LargeurCase/2)] = 5
    afficher_map(canvas)

    