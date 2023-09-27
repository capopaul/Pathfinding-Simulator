#----------------
from random import random
import numpy as np
#----------------
from Usefull.fonctionsFichier import *

#----------------

def generer_labyrinthe(canvas):
        
    Linitial = int(config().ReturnValue("LargeurLab"))
    Hinitial = int(config().ReturnValue("HauteurLab"))

    # Algorythme qui genere le labyrinthe en cassant les murs autour de lui.
    #Fonctionnement:
    #   Je choisis une direction Haut bas droite gauche
    #       Si la case est visitee:
    #           je fais rien
    #       Sinon:
    #           je casse le mur
    lab = np.array([[1] * (Linitial*2-1) for _ in range(Hinitial*2-1)])

    nbCaseTraitee = 1
    Xcase = 0
    Ycase = 0
    lab[0][0] = 0
    while nbCaseTraitee != Linitial * Hinitial:
        r = int(4*random()+1)
        if ( r == 1):
            if(Xcase+2 <= Linitial*2-1):
                Xcase = Xcase+2
            else: continue
        if ( r == 2):
            if(Xcase-2 >= 0):
                Xcase = Xcase-2
            else: continue
        if ( r == 3):
            if(Ycase-2 >= 0):
                Ycase = Ycase-2
            else: continue
        if ( r == 4):
            if(Ycase+2 <= Hinitial*2-1):
                Ycase = Ycase+2
            else: continue
        if( lab[Ycase][Xcase] == 1):
            lab[Ycase][Xcase] = 0
            if ( r == 1):
                lab[Ycase][Xcase-1] = 0
            if ( r == 2):
                lab[Ycase][Xcase+1] = 0
            if ( r == 3):
                lab[Ycase+1][Xcase] = 0
            if ( r == 4):
                lab[Ycase-1][Xcase] = 0
            nbCaseTraitee += 1
           
    canvas.coordStartRobot = [0,0]
    canvas.coordEndRobot = [int(config().ReturnValue("HauteurLab"))*2-2 , int(config().ReturnValue("LargeurLab"))*2-2]
    lab[0,0] = 4
    lab[int(config().ReturnValue("HauteurLab"))*2-2 , int(config().ReturnValue("LargeurLab"))*2-2] = 5
    return lab