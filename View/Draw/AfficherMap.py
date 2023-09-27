#----------------
from random import random
import threading

#----------------
from Usefull.fonctionsFichier import *
from View.objects.cube import *
from View.Draw.elementsBase import *

#----------------

def afficher_map(canvas):
    
    canvas.coordStartRobot = np.column_stack((np.flip(np.where(canvas.tableauMap == 4)))).flatten()
    canvas.coordEndRobot = np.column_stack((np.flip(np.where(canvas.tableauMap == 5)))).flatten()
         
    canvas.Mur = np.array(np.column_stack((np.flip(np.where(canvas.tableauMap == 1)))), np.float32).flatten()
    canvas.Marge = np.array(np.column_stack((np.flip(np.where(canvas.tableauMap == 2)))), np.float32).flatten()
    canvas.actualiser = True
        
    
    
    