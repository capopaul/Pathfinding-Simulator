# -*- coding: utf-8 -*-

import numpy as np
import threading

#----------------------------------
from Model.usefull import *
from Usefull.afficher import *

#----------------------------------


class AlgoAV4(threading.Thread):
    def __init__(self, canvas):
        threading.Thread.__init__(self)
        #Je verifie que les valeurs de depart et d'arrive son sur la map:
        if existance(canvas):
            self.canvas = canvas
            #Open List contient les valeurs des cases � tester
            self.OpenList = np.zeros((len(self.canvas.tableauMap[0]), len(self.canvas.tableauMap), 5))
            #CloseList contient les cases testees: [g,h,f, parentx, parent z]
            self.CloseList = np.zeros((len(self.canvas.tableauMap[0]), len(self.canvas.tableauMap), 5))
            self.CurrentSell = np.array([int(self.canvas.coordStartRobot[0]), int(self.canvas.coordStartRobot[1])])
            #                                            G,     H,                        F,                        
            self.CloseList[tuple(self.CurrentSell)] = [ 0, self._H(self.CurrentSell), self._H(self.CurrentSell), 
                                                       int(self.canvas.coordStartRobot[0]), int(self.canvas.coordStartRobot[1])]
                                                        # ParentX                        Parent Z
            
            self.statut = 0 #  0 En cours | 1 Fini | 2 Pas de solution
            
            self.canvas.simulation = True
    
    
    def run(self):
        if existance(self.canvas):
            #Boucle Principale
            while (self.CurrentSell[0] != self.canvas.coordEndRobot[0] or self.CurrentSell[1] != self.canvas.coordEndRobot[1]) and self.statut == 0:
                self._nextTourAction()
            
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
        
        OpenListF = self.OpenList[:,:,2]
        i,j = np.where(OpenListF == np.min(OpenListF[np.nonzero(OpenListF)]))
        
        self.CurrentSell = [i[0],j[0]]
        
        self.CloseList[tuple(self.CurrentSell)] = self.OpenList[tuple(self.CurrentSell)]
        self.OpenList[tuple(self.CurrentSell)] = [0 , 0, 0, 0, 0]
        self.canvas.coordRobot = self.CurrentSell
    
    
    def _solution(self):
        if self.statut == 1:    
            self._solution = np.array([[int(self.canvas.coordEndRobot[0]), int(self.canvas.coordEndRobot[1])]])
            self.CurrentSell = np.array([int(self.canvas.coordEndRobot[0]), int(self.canvas.coordEndRobot[1])])
            
            while self.CurrentSell[0] != self.canvas.coordStartRobot[0] or self.CurrentSell[1] != self.canvas.coordStartRobot[1]:
                self._value = self.CloseList[tuple(self.CurrentSell)]
                self._solution = np.append(self._solution, [[self._value[3], self._value[4]]], axis = 0)
                
                self.CurrentSell[0] = self._value[3]
                self.CurrentSell[1] = self._value[4]
                
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
        #print("_sellVide",_sellVide)
        
        #print(ListeContenuDansCloseList(CloseList, _sellVide))
        
        _selltoTreat = differenceListe(_sellVide,ListeContenuDansCloseList(self.CloseList, _sellVide))
        
        #print("_selltoTreat", _selltoTreat)
        #_sellInOpenList = ListeContenuDansCloseList(self.OpenList, _selltoTreat)
        #print("_sellInOpenList", _sellInOpenList)
        #_sellToAdd = differenceListe(_selltoTreat,_sellInOpenList)
        #print("_sellToAdd", _sellToAdd)
        for sell in _selltoTreat:
            _g = self._G(self.CloseList, sell, self.CurrentSell)
            if(_g <  self.OpenList[sell[0], sell[1],0] or self.OpenList[sell[0], sell[1],0] == 0 ):
                _h = self._H(sell)
                _f = _g + _h
                _parentX = self.CurrentSell[0]
                _parentZ = self.CurrentSell[1]
                self.OpenList[tuple(sell)] = [ _g, _h, _f, _parentX, _parentZ]
                

    def _caseVideAutourCanvasMap(self):
    
        PossibleSell = np.array([[0,0]])
        
        _extremite = np.array([[1, 0], [-1, 0],
                             [0, 1], [0, -1],
                             [1, 1], [-1, -1],
                             [1, -1], [-1, 1]])
        
        for edit in _extremite:
                        
            _x = self.CurrentSell[0] + edit[0]
            _z = self.CurrentSell[1] + edit[1]
            #1 on verifie que la case existe
            if ((_x) >= 0 and (_x) < (len(self.canvas.tableauMap[0])) and 
            (_z) >=0 and (_z) < (len(self.canvas.tableauMap))):
                # 2 on verifie que ce n'est pas un mur
                if self.canvas.tableauMap[_z][_x] != 1 and self.canvas.tableauMap[_z][_x] != 2:
                    PossibleSell = np.concatenate((PossibleSell, [[_x, _z]]))
        return np.delete(PossibleSell, 0, axis=0)
    
    
    def _H(self, sell):
        return abs(self.canvas.coordEndRobot[0]-sell[0])+abs(self.canvas.coordEndRobot[1]-sell[1])
    
    
    def _G(self, CloseList, sell, parent):
        _gTotal = CloseList[parent[0], parent[1],0]
        _gAdd = 0
        if abs(sell[0]-parent[0]) != 0:
            _gAdd += 1
        if abs(sell[1]-parent[1]) != 0:
            _gAdd += 1
        if _gAdd == 2:
            _gAdd = 1.4
        _gTotal += _gAdd
        return _gTotal