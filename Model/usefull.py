# -*- coding: utf-8 -*-

#----------------------------------
import numpy as np
import math
#----------------------------------
from Usefull.afficher import *

#----------------------------------
def coordEndRobot(canvas, point):
    if MapContainsPoint(canvas, point):
        ancienneCoords = np.column_stack((np.flip(np.where(canvas.tableauMap == 5)))).flatten()
        try:
            canvas.tableauMap[ancienneCoords[1], ancienneCoords[0]] = 0
        except IndexError:pass
        canvas.tableauMap[point[1],point[0]] = 5
        canvas.coordEndRobot = point
    else:
        Afficher("Erreur veuillez configurer le point de départ et d arrivée")
def coordStartRobot(canvas, point):
    if MapContainsPoint(canvas, point):
        ancienneCoords = np.column_stack((np.flip(np.where(canvas.tableauMap == 4)))).flatten()
        canvas.tableauMap[ancienneCoords[1], ancienneCoords[0]] = 0
        canvas.tableauMap[point[1],point[0]] = 4
        canvas.coordStartRobot = point
    else:
        return False
def existance(canvas):
    if (MapContainsPoint(canvas, canvas.coordStartRobot) and MapContainsPoint(canvas, canvas.coordEndRobot)):
        return True
    else:
        Afficher("Erreur veuillez configurer le point de départ et d arrivée")
        return False


def MapContainsPoint(canvas, point):
    if (point[0] < len(canvas.tableauMap[0]) and point[0] >= 0 and 
        point[1] < len(canvas.tableauMap) and point[1] >= 0):
        return True
    else:
        return False
    
'''    
def differenceListe(Liste1, Liste2):
    #Liste 1 moins liste 2
    if len(np.shape(Liste1)) == len(np.shape(Liste2)):   
        ListeDifference = np.copy(Liste1)
        for indexListe2 in range(len(Liste2)):
            for indexListeDifference in range(len(ListeDifference)):
                if np.array_equal(Liste2[indexListe2], ListeDifference[indexListeDifference]):
                    ListeDifference = np.delete(ListeDifference, indexListeDifference, axis=0)
                    break
        return (ListeDifference)
    else:
        return ValueError  '''
    
def differenceListe(Liste1, Liste2):
    #Liste 1 moins liste 2
    if len(np.shape(Liste1)) == len(np.shape(Liste2)):   
        ListeDifference = np.copy(Liste1)
        for indexListe2 in range(len(Liste2)):
            for indexListeDifference in range(len(ListeDifference)):
                if np.array_equal(Liste2[indexListe2], ListeDifference[indexListeDifference]):
                    ListeDifference = np.delete(ListeDifference, indexListeDifference, axis=0)
                    break
        return (ListeDifference)
    else:
        return ValueError    

def ListeContenuDansCloseList(CloseList, listeB): #Marche aussi pour OpenList
    ListeContenu = np.array([[0,0]])
    for coord in listeB:
        contient = False
        for i in range(CloseList.shape[2]):
            #print("coord[0],coord[1], i", coord[0],coord[1], i)
            if CloseList[coord[0],coord[1], i] != 0:
                contient = True
                break
        if contient:        
            ListeContenu = np.concatenate((ListeContenu, [coord]))
    return( np.delete(ListeContenu, 0, axis=0))
           
def PlusPetitFOpenList(self):        
    newCurrentSell = np.array([1,1])
    _minF = 15000000
    for x in range(len(self.OpenList)):
        for z in range(len(self.OpenList[1])):
            if self.OpenList[x, z, 0] != 0:
                if self.OpenList[x, z, 2] < _minF:
                    _minF = self.OpenList[x, z, 2]
                    newCurrentSell[0] = x
                    newCurrentSell[1] = z
    if _minF == 15000000:
        self.statut = 2
    return newCurrentSell

def vecteurSolution(solution):
    
    retourList = np.array([[0,0]])
    for index in range(1, len(solution)):
        retourList = np.concatenate((retourList, [solution[index]-solution[index-1]]))
    return np.delete(retourList, 0, axis=0)
  
def nextPointSolution(vecteurSolution, pointSolution):
    _pointSolution = np.array(pointSolution, dtype = np.uint32)
    retourVecteurList = np.array([[0,0]])
    indexList = np.array([0])
    memo = vecteurSolution[0]
    
    for index in range(1, len(vecteurSolution)):
        if vecteurSolution[index,0] == vecteurSolution[index-1,0] and vecteurSolution[index,1] == vecteurSolution[index-1,1]:
            memo = vecteurSolution[index]+memo
        else:
            retourVecteurList = np.concatenate((retourVecteurList, [memo]))
            indexList = np.append(indexList, index)
            memo = vecteurSolution[index]
    retourVecteurList = np.concatenate((retourVecteurList, [memo]))
    indexList = np.append(indexList, len(vecteurSolution))

    return np.delete(retourVecteurList, 0, axis=0), _pointSolution[np.array(indexList, dtype = np.uint32)]
    
    
def angleVecteur(vecteur):
    angle = 0
    if vecteur[0] == 0:
        if vecteur[1] > 0:
            angle = math.pi/2
        else:
            angle = - math.pi/2
    elif vecteur[0] > 0:
        angle = math.atan(vecteur[1]/vecteur[0])
    else:
        angle = math.atan(vecteur[1]/vecteur[0])+math.pi
    return angle

def normeVecteur(vecteur):
    return math.sqrt(vecteur[0]**2+vecteur[1]**2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


