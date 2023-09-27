# -*- coding: utf-8 -*-
import threading
import numpy as np
import time as t
import math
#----------------------------------
from Model.usefull import *
from Usefull.afficher import *
from View.initRendu.initAlgo import *
#----------------------------------


class AlgoAV7(threading.Thread):
    def __init__(self, canvas):
        threading.Thread.__init__(self)
        #Je verifie que les valeurs de depart et d'arrive son sur la map:
        if existance(canvas):
            self.canvas = canvas
            #Open List contient les valeurs des cases � tester
            self.OpenList = np.zeros((len(self.canvas.tableauMap[0]), len(self.canvas.tableauMap), 6))
            #CloseList contient les cases testees: [g,h, P, f, parentx, parent z]
            self.CloseList = np.zeros((len(self.canvas.tableauMap[0]), len(self.canvas.tableauMap), 6))
            self.CurrentSell = np.array([int(self.canvas.coordStartRobot[0]), int(self.canvas.coordStartRobot[1])])
            #                                            G,     H,                    P,    F,                        
            self.CloseList[tuple(self.CurrentSell)] = [ 0, self._H(self.CurrentSell), 0,  self._H(self.CurrentSell), 
                                                       int(self.canvas.coordStartRobot[0]), int(self.canvas.coordStartRobot[1])]
                                                        # ParentX                        Parent Z
            
            self.statut = 0 #  0 init faite | 1 Fini | 2 Pas de solution | 3 recherche en cours
            self.canvas.afficherAlgo = 0
            self.canvas.simulation = True
    def run(self):
        if existance(self.canvas):
            #Boucle Principale
            self.statut = 3
            while (self.CurrentSell[0] != self.canvas.coordEndRobot[0] or self.CurrentSell[1] != self.canvas.coordEndRobot[1]) and self.statut == 3:
                self._nextTourAction()

            self.statut = 0
            if self.CurrentSell[0] == self.canvas.coordEndRobot[0] and self.CurrentSell[1] == self.canvas.coordEndRobot[1]:          
                self.statut = 1
                self._solution()
            else:
                Afficher("Pas de solution trouvée !")
                self.canvas.afficherSolution = False    
    
    
    def nextTourAction(self):
        if existance(self.canvas):
            if self.statut == 0:
                if self.CurrentSell[0] != self.canvas.coordEndRobot[0] or self.CurrentSell[1] != self.canvas.coordEndRobot[1]:
                    self._nextTourAction()
                else:
                    self.statut = 1
                    Afficher("Chemin trouvé !")
            elif self.statut == 1:
                Afficher("Chemin trouvé !")
            elif self.statut == 2:
                Afficher("Pas de solution trouvée !")
                
           
    def _nextTourAction(self):
        
        self._addNewValuesToOpenList()
        
        OpenListF = self.OpenList[:,:,3]
        i,j = np.where(OpenListF == np.min(OpenListF[np.nonzero(OpenListF)]))
        
        self.CurrentSell = [i[0],j[0]]
        self.CloseList[tuple(self.CurrentSell)] = self.OpenList[tuple(self.CurrentSell)]
        self.OpenList[tuple(self.CurrentSell)] = [0 , 0, 0, 0, 0, 0]

        while self.canvas.nextAlgoCube != True:
            pass
        
        
        self.canvas.AlgoCubeNewValue = np.array(np.append(self.canvas.AlgoCubeNewValue, [tuple(self.CurrentSell)]), dtype=np.float32).flatten() 
        
        self.canvas.coordRobot = self.CurrentSell

    
    def _solution(self):
        if self.statut == 1:    
            self._solution = np.array([[int(self.canvas.coordEndRobot[0]), int(self.canvas.coordEndRobot[1])]])
            self.CurrentSell = np.array([int(self.canvas.coordEndRobot[0]), int(self.canvas.coordEndRobot[1])])
            
            while self.CurrentSell[0] != self.canvas.coordStartRobot[0] or self.CurrentSell[1] != self.canvas.coordStartRobot[1]:
                self._value = self.CloseList[tuple(self.CurrentSell)]
                self._solution = np.append(self._solution, [[self._value[4], self._value[5]]], axis = 0)
                
                self.CurrentSell[0] = self._value[4]
                self.CurrentSell[1] = self._value[5]
                
            _pointSolution = self._solution[::-1]
            _vecteurSolution = vecteurSolution(_pointSolution)
            self.canvas.vecteurSolution, self.canvas.pointSolution = nextPointSolution(_vecteurSolution, _pointSolution)
            
            self.canvas.afficherSolution = 0
            Afficher(("La distance du chemin (D) est : "+str(self.CloseList[self.canvas.coordEndRobot[0], self.canvas.coordEndRobot[1], 0])+
                      "\nLes penalitées totales (P) sont de "+str(self.CloseList[self.canvas.coordEndRobot[0], self.canvas.coordEndRobot[1], 2])))
            
            
    def _addNewValuesToOpenList(self):
        #Tester si les cases autour de currentSell existe: retourner les cases differentes des murs
        #Supprimer celle qui sont d�j� dans la closelist
        #Verifier qu'elle n'existe pas dans openlist et les ajouter
        #Si elle existe: Verifier que le chemin le plus court est bien avec la nouvelle case
        #Sinon ne rien faire
        
        _sellVide = self._caseVideAutourCanvasMap()
        _sellInCloseList = ListeContenuDansCloseList(self.CloseList, _sellVide)
        _selltoTreat = differenceListe(_sellVide,ListeContenuDansCloseList(self.CloseList, _sellVide))
        
        for sell in _selltoTreat:
            _d = self._D(self.CloseList, sell, self.CurrentSell)
            _h = self._H(sell)
            _p = self._P(sell)
            _f = _d + _p +_h
            
            if(_f <  self.OpenList[sell[0], sell[1],3] or self.OpenList[sell[0], sell[1],3] == 0 ):
                _parentX = self.CurrentSell[0]
                _parentZ = self.CurrentSell[1]
                self.OpenList[tuple(sell)] = [ _d, _h, _p, _f, _parentX, _parentZ] 
                     
        for sell in _sellInCloseList:
            _d = self._D(self.CloseList, sell, self.CurrentSell)
            _h = self._H(sell)
            _p = self._P(sell)
            _f = _d + _p
            
            if(_f <  self.CloseList[sell[0], sell[1],0]+self.CloseList[sell[0], sell[1],2]):
                _f += _h
                _parentX = self.CurrentSell[0]
                _parentZ = self.CurrentSell[1]
                self.CloseList[tuple(sell)] = [ _d, _h, _p, _f, _parentX, _parentZ]   
              
    def _caseVideAutourCanvasMap(self):
    
        PossibleSell = np.array([[0,0]])
        
        _extremite = np.array([[1, 0], [-1, 0],
                             [0, 1], [0, -1],
                             [1, 1], [-1, -1],
                             [1, -1], [-1, 1]])
        
        for edit in _extremite:
                        
            _x,_z = self.CurrentSell + edit
            #1 on verifie que la case existe
            if ((_x) >= 0 and (_x) < (len(self.canvas.tableauMap[0])) and 
            (_z) >=0 and (_z) < (len(self.canvas.tableauMap))):
                # 2 on verifie que ce n'est pas un mur
                if self.canvas.tableauMap[_z][_x] != 1 and self.canvas.tableauMap[_z][_x] != 2:
                    PossibleSell = np.concatenate((PossibleSell, [[_x, _z]]))
        return np.delete(PossibleSell, 0, axis=0)
    
    
    def _H(self, sell):
        return abs(self.canvas.coordEndRobot[0]-sell[0])+abs(self.canvas.coordEndRobot[1]-sell[1])
    
    def _P(self, sell):
        
        penalite = 0
        
        
        
        previusStep = self.CurrentSell-self.CloseList[self.CurrentSell[0], self.CurrentSell[1], 4:6]
        normepreviusStep = math.sqrt(previusStep[0]**2+previusStep[1]**2)
        
        if normepreviusStep != 0:
            
            step = sell-self.CurrentSell
            normeStep = math.sqrt(step[0]**2+step[1]**2)
            
            sclaire1 = step[0]*previusStep[0]+step[1]*previusStep[1]
            sclaire2 = normeStep*normepreviusStep
            
            result = abs(math.degrees(math.acos(sclaire1/sclaire2)))
            if result <= 1:
                penalite = -0.5
            elif result <= 46:
                penalite = 0.7
            elif result <= 91:
                penalite = 1.2
            elif result >91:
                penalite = 4
        return self.CloseList[self.CurrentSell[0], self.CurrentSell[1],2]+penalite
    
    def _D(self, CloseList, sell, parent):
        _dTotal = CloseList[parent[0], parent[1],0]
        _dAdd = 0
        if abs(sell[0]-parent[0]) != 0:
            _dAdd += 1
        if abs(sell[1]-parent[1]) != 0:
            _dAdd += 1
        if _dAdd == 2:
            _dAdd = 1.4
        _dTotal += _dAdd
        return _dTotal