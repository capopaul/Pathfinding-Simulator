#----------------------------------
import wx
import keyboard
import math
import numpy as np

#----------------------------------
from View.objects.cube import *
from View.Draw.AfficherMap import *
from View.initRendu.initEditMode import initEditMode
#----------------------------------

def eventManager(canvas):
    def MouseMiddleEvent(evt):
        if canvas.editMode:
            canvas.editMode = False
            
            canvas.SetCursor(wx.StockCursor(wx.CURSOR_ARROW)) 
        else:
            initEditMode(canvas)
            canvas.editMode = True
            canvas.SetCursor(wx.StockCursor(wx.CURSOR_BLANK)) 
            
    def MouseMotionEvent(evt):
        if canvas.editMode or wx.MouseState.LeftIsDown(evt):
            mouseCoordRelative = canvas.ScreenToClient(wx.GetMousePosition())- canvas.GetSize()/2
            difference = mouseCoordRelative- canvas._memoMousePosition
            if abs(np.linalg.norm(difference)) < 30:
                canvas._theta += math.atan(difference[0]/canvas.sensibilite)
                canvas._phi += math.atan(difference[1]/canvas.sensibilite)
                
                if(canvas._phi > (math.pi/2)-0.05):
                    canvas._phi = (math.pi/2)-0.05
                elif(canvas._phi < -((math.pi/2)-0.05)):
                    canvas._phi = -((math.pi/2)-0.05)
                    
                canvas._orientation[0] = math.sin(-canvas._theta)*math.cos(canvas._phi)
                canvas._orientation[1] = -math.sin(canvas._phi)
                canvas._orientation[2] = math.cos(-canvas._theta)*math.cos(canvas._phi)
                canvas.cameraPointCible = canvas.cameraPosition + canvas._orientation
            canvas._memoMousePosition = mouseCoordRelative
    def MouseLeftEvent(evt):
        if((canvas.editMode == True) and (canvas.ligneMode == False)):
            t = (0.2-canvas.cameraPosition[1])/(canvas.cameraPointCible[1]-canvas.cameraPosition[1])
            point = [int(canvas.cameraPosition[0]+(canvas.cameraPointCible[0]-canvas.cameraPosition[0])*t),
                   int(canvas.cameraPosition[2]+(canvas.cameraPointCible[2]-canvas.cameraPosition[2])*t),
                   ]
            if(canvas.tableauMap[point[1],point[0]] == 0):
                canvas.tableauMap[point[1],point[0]] = 1
                afficher_map(canvas)
                
        if ((canvas.editMode == True) and (canvas.ligneMode == True)):
            t = (0.2-canvas.cameraPosition[1])/(canvas.cameraPointCible[1]-canvas.cameraPosition[1])
            point = np.array([int(canvas.cameraPosition[0]+(canvas.cameraPointCible[0]-canvas.cameraPosition[0])*t),
                   int(canvas.cameraPosition[2]+(canvas.cameraPointCible[2]-canvas.cameraPosition[2])*t)
                   ])
            canvas.coordLigne = np.concatenate((canvas.coordLigne, point.flatten()))
            canvas.actualiser = True
    def MouseRightEvent(evt):
        if ((canvas.editMode == True) and (canvas.ligneMode == False)):
            t = (0.2-canvas.cameraPosition[1])/(canvas.cameraPointCible[1]-canvas.cameraPosition[1])
            point = [int(canvas.cameraPosition[0]+(canvas.cameraPointCible[0]-canvas.cameraPosition[0])*t),
                   int(canvas.cameraPosition[2]+(canvas.cameraPointCible[2]-canvas.cameraPosition[2])*t),
                   ]
            if(canvas.tableauMap[point[1],point[0]] == 1):
                canvas.tableauMap[point[1],point[0]] = 0
                afficher_map(canvas)
        if ((canvas.editMode == True) and (canvas.ligneMode == True)):
            t = (0.2-canvas.cameraPosition[1])/(canvas.cameraPointCible[1]-canvas.cameraPosition[1])
            point = [int(canvas.cameraPosition[0]+(canvas.cameraPointCible[0]-canvas.cameraPosition[0])*t),
                   int(canvas.cameraPosition[2]+(canvas.cameraPointCible[2]-canvas.cameraPosition[2])*t),
                   ]
            
            ligne = canvas.coordLigne.reshape(int(len(canvas.coordLigne)/2), 2)
            i,j = np.where(ligne == point[0])
            
            for ind in range (len(i)):
                if point[1] == ligne[i[ind],1]:
                    ligne = ligne.flatten()
                    ligne = np.delete(ligne, 2*i[ind])
                    ligne = np.delete(ligne, 2*i[ind])
                    break
            
            ligne = ligne.flatten()
            canvas.coordLigne = ligne
            canvas.actualiser = True
            
    def clavier(canvas):
        def SiDroite():
            if keyboard.is_pressed('d'):
                return True
            return False
        def SiGauche():
            if keyboard.is_pressed('q'):
                return True
            return False
        def SiDescendre():
            if keyboard.is_pressed('shift'): #Shift
                return True
            else: return False
        def SiMonter():
            if keyboard.is_pressed('space'): #Espace
                return True
            else: return False
        def SiReculer():
            if keyboard.is_pressed('s'):
                return True
            else: return False
        def SiAvancer():
            if keyboard.is_pressed('z') :
                return True
            else: return False
        if keyboard.is_pressed('k'):
            if canvas.ligneMode:
                canvas.ligneMode = False
            else:
                canvas.ligneMode = True
        if SiAvancer():
            canvas.cameraPosition += canvas._orientation*canvas.deplacement
            canvas.cameraPointCible += canvas._orientation*canvas.deplacement
        elif SiReculer():
            canvas.cameraPosition -= canvas.deplacement*canvas._orientation
            canvas.cameraPointCible -= canvas.deplacement*canvas._orientation
        if SiDroite():
            canvas._deplacementLateral = np.cross(canvas._orientation, canvas.axeVertical)
            canvas.cameraPosition += canvas._deplacementLateral*canvas.deplacement
            canvas.cameraPointCible += canvas._deplacementLateral*canvas.deplacement
        elif SiGauche():
            canvas._deplacementLateral = np.cross(canvas._orientation, canvas.axeVertical)
            canvas.cameraPosition -= canvas._deplacementLateral*canvas.deplacement
            canvas.cameraPointCible -= canvas._deplacementLateral*canvas.deplacement
        if SiMonter():
            canvas.cameraPosition[1] += canvas.deplacement
            canvas.cameraPointCible[1] += canvas.deplacement
        elif SiDescendre():
            canvas.cameraPosition[1] -= canvas.deplacement
            canvas.cameraPointCible[1] -= canvas.deplacement
    canvas.Bind(wx.EVT_LEFT_DOWN, MouseLeftEvent)
    canvas.Bind(wx.EVT_RIGHT_DOWN, MouseRightEvent)
    canvas.Bind(wx.EVT_MOTION, MouseMotionEvent)
    canvas.Bind(wx.EVT_MIDDLE_DOWN, MouseMiddleEvent)
    clavier(canvas)
