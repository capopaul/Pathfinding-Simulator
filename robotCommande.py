# -*- coding: utf-8 -*-

#----------------------------------
import math
import serial
import numpy as np
import math as m
from threading import Thread
import time

#----------------------------------
from Usefull.fonctionsFichier import *

#----------------------------------

class SerialInteract(Thread):

    """Thread chargement desimplement d'afficher une lettre dans la console."""
    """
    
    Da; Db, Gb, Ga,
    
    
    1400;-1400;-1400;1400;
    1526;-1400;-1400;1526;
    
    
"""
    def __init__(self, canvas):
        Thread.__init__(self)
        self.canvas = canvas
        self.statut = 0
        try:
            # -1: erreur initialisation : 0: valeur au depart: 1 = initialisation faite avec succès ; 2 traitement en cours thread lancé; 3 : fini
            self.port_serie = serial.Serial(port=config().Port,baudrate=9600,timeout=0.01)
            
            self.PosRoue = np.array([[11,10],[11,-10],[-11,-10],[-11,10]])
        
            self.ConstanteRotation = 26.31/500
            
            self.MatTransVec2Wheel = np.matrix([[1,-1,-210],[1,1,-210],[1,-1,210],[1,1,210]])
            
            self.MatTransWheel2Vec = np.matrix([[0.25,0.25,0.25,0.25],[-0.25,0.25,-0.25,0.25],[-1./(4.*210.),-1/(4.*210.),1./(4.*210.),1./(4.*210.)]])
            
            self.Kp=0.2
            
            self.Ki=0
            
            self.Kd=0
            
            self.taille = float(config().Reel_Echelle)
            self.CoeffRotation = float(config().CoeffRotation)
            self.statut = 1
        except serial.serialutil.SerialException:
            self.statut = -1
            print("Branchez le dispositif de communication")
            
        
        
    def run(self):
        """Code  exécuté pendant l'exécution du thread."""
        
        def distance(xa, ya, xb, yb):
            return math.sqrt(((xb-xa)**2)+((yb-ya)**2))
        
        if self.statut == 1:
            
            timer = 0
            Tlast = time.time()
            self.canvas.simulationReel = True
            
            #compteur de point
            i = 0
            
            
            listeVecteur = self.taille*np.array(self.canvas.pointSolution.flatten())
            RobotPosition = [(-1)*self.taille*self.canvas.coordRobot[0], self.taille*self.canvas.coordRobot[1], 0]
            try:
                RobotPoint = np.array([listeVecteur[i], listeVecteur[i+1],0], dtype=np.uint32)
            
                
                rotation = self.CoeffRotation*RobotPoint[2]
                RobotAim = np.array([(-1)*RobotPoint[0], RobotPoint[1], rotation])
                LastErreur =  np.matrix([[0],[0],[0]])
                
            except IndexError:
                self.statut = -1
                self.port_serie.close()
                return
            time.sleep(2)
            self.statut = 2
            
            while self.canvas.simulationReel:
                
                
                    if math.fabs(distance(RobotPosition[0], RobotPosition[1], RobotAim[0], RobotAim[1])) <= float(config().DistanceChangePoint):
                        i += 2
                        if len(listeVecteur) > i:
                            RobotPoint = [listeVecteur[i], listeVecteur[i+1],0]
                            rotation = self.CoeffRotation*RobotPoint[2]
                            RobotAim = np.array([(-1)*RobotPoint[0], RobotPoint[1], rotation])
                        else:
                            self.canvas.simulationReel = False
                    try:               
                        ligne = self.port_serie.readline().decode('utf-8').split(";")
                    except UnicodeDecodeError:
                        print("Erreur bizarre qui sort de je ne sais ou")
                        break
                    if(len(ligne) == 5):
                        
                        Tnow = time.time()
                        
                        
                        Tdelta = Tnow - Tlast
                    
                        MatWheelRecup = np.matrix([[-int(ligne[3])],[-int(ligne[2])],[int(ligne[1])],[int(ligne[0])]])/14
    
                        MatDirectionVector = ( self.MatTransWheel2Vec * MatWheelRecup ) / 28
                        
                        if self.canvas.ligneDetectee == False:
                        
                            RobotPosition[0] += MatDirectionVector[0,0]*Tdelta
                            RobotPosition[1] += MatDirectionVector[1,0]*Tdelta
                            RobotPosition[2] += MatDirectionVector[2,0]*Tdelta
                            self.canvas.coordRobot = [-RobotPosition[0]/self.taille,RobotPosition[1]/self.taille]
                        else:
                            RobotPosition[0] = (-1)*self.taille*self.canvas.coordRobot[0]
                            RobotPosition[1] = self.taille*self.canvas.coordRobot[1]
                        
                        
                        Tlast = time.time()
                    
                    x = RobotAim[0]- RobotPosition[0]
                    y = RobotAim[1]- RobotPosition[1]
                    t = RobotAim[2]- RobotPosition[2]
                    

                    Erreur = np.matrix([[x],[y],[t]])
    
    
                    DeltaErreur = Erreur - LastErreur
                    
                    MatTranslat = ( Erreur * self.Kp + DeltaErreur*self.Kd )

                    LastErreur = Erreur
                    
                    MatWheelVel = ( self.MatTransVec2Wheel * MatTranslat ) *28*14
                    
                    commande = str(int(MatWheelVel[3,0]))+";"+str(int(MatWheelVel[2,0]))+";"+str(int(-MatWheelVel[1,0]))+";"+str(int(-MatWheelVel[0,0]))+";"
                    
                    self.port_serie.write(commande.encode("utf-8"))
                    
                    time.sleep(0.05)
                    
                    timer+=0.05
            
            #Fin de la boucle principale
            commande = "0;0;0;0;"
            for _ in range(5):
                self.port_serie.write(commande.encode("utf-8"))
                time.sleep(0.03)
                
            self.port_serie.close()
            self.statut = 3   
        else:
            print("Désolé mais l'initialisation n'a pas fonctionnée")

