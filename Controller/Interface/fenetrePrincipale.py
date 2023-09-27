# -*- coding: utf-8 -*-

#----------------------------------
import wx
from OpenGL.GL import glViewport
import numpy
import threading

#----------------------------------
from View.OpenGLCanvas import OpenGLCanvas
from Controller.Interface.menuBar.MenuBar_Principal import MenuBar_Principale
from Usefull.fonctionsFichier import *
from Model.Algorithmes.AlgoAV1 import *
from Model.Algorithmes.AlgoAV2 import *
from Model.Algorithmes.AlgoAV3 import *
from Model.Algorithmes.AlgoAV4 import *
from Model.Algorithmes.AlgoAV5 import *
from Model.Algorithmes.AlgoAV6 import *
from Model.Algorithmes.AlgoAV7 import *
from Controller.Interface.parametres import *
from Usefull.afficher import *
from robotView import *

from robotCommande import SerialInteract

#----------------------------------
class PanelFrame_Principale(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        #Classe de l'aglo
        self.algo = 0
        
        sizer = wx.GridBagSizer(5, 5)
        
        path = "Saves/ressources/"
        
        iconPlay = wx.Bitmap(path+"play.png")
        iconRePlay = wx.Bitmap(path+"replay.png")
        iconStop = wx.Bitmap(path+"stop.png")
        iconStart = wx.Bitmap(path+"start.png")
        iconFlecheDroite = wx.Bitmap(path+"flechedroite.png")
        iconVue = wx.Bitmap(path+"vue.png")
        iconDoSolution = wx.Bitmap(path+"dosolution.png")
        iconShowSolution = wx.Bitmap(path+"showsolution.png")
        iconParametre = wx.Bitmap(path+"parametre.png")
        
        self.boutonParametre = wx.BitmapButton(self, -1, bitmap = iconParametre , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.parametre, self.boutonParametre)
        sizer.Add(self.boutonParametre, pos=(0, 0))
        
        
        self.listeMesAlgo = ["A* version 7","A* version 1","A* version 2 - Pas de ligne droite", "A* version 3 - Pas de diagonale", "A* version 4 - Problème de temps", 
                             "A* version 5 - Problème temps resolu", "A* version 6 - Pénalité"]
        self.entryAlgoBox = wx.ListBox(self, -1, size=(240,35), choices=self.listeMesAlgo, style=wx.LB_SINGLE, name="Algorithme")
        sizer.Add(self.entryAlgoBox, pos=(0,1))
        self.entryAlgoBox.SetFocus()
        
        self.boutonPlay = wx.BitmapButton(self, -1, bitmap = iconPlay , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.play, self.boutonPlay)
        sizer.Add(self.boutonPlay, pos=(0, 2))
        
        self.boutonRePlay = wx.BitmapButton(self, -1, bitmap = iconRePlay , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.boutonRePlay.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.replay, self.boutonRePlay)
        sizer.Add(self.boutonRePlay, pos=(0, 3))
        
        self.boutonStop = wx.BitmapButton(self, -1, bitmap=iconStop, style=wx.BUFFER_USES_SHARED_BUFFER)
        self.boutonStop.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.stop, self.boutonStop)
        sizer.Add(self.boutonStop, pos=(0, 4))
        
        self.boutonFlecheDroite = wx.BitmapButton(self, -1, bitmap = iconFlecheDroite , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.NextStep, self.boutonFlecheDroite)
        sizer.Add(self.boutonFlecheDroite, pos=(0, 5))
        
        self.boutonRobotView = wx.BitmapButton(self, -1, bitmap = iconVue , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.robotView, self.boutonRobotView)
        sizer.Add(self.boutonRobotView, pos=(0, 6))
        
        self.boutonShowSolution = wx.BitmapButton(self, -1, bitmap = iconShowSolution , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.ShowSolution, self.boutonShowSolution)
        sizer.Add(self.boutonShowSolution, pos=(0, 7))
        
        self.boutonDoSolution = wx.BitmapButton(self, -1, bitmap = iconDoSolution , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.DoSolution, self.boutonDoSolution)
        sizer.Add(self.boutonDoSolution, pos=(0, 8))
             
        
        self.boutonStart = wx.BitmapButton(self, -1, bitmap = iconStart , style=wx.BUFFER_USES_SHARED_BUFFER)
        self.Bind(wx.EVT_BUTTON, self.Start, self.boutonStart)
        sizer.Add(self.boutonStart, pos=(0, 9))
        
        self.boutonStopRobot = wx.BitmapButton(self, -1, bitmap=iconStop, style=wx.BUFFER_USES_SHARED_BUFFER)
        self.boutonStopRobot.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.stopRobot, self.boutonStopRobot)
        sizer.Add(self.boutonStopRobot, pos=(0, 10))
        
             
        self.canvas = OpenGLCanvas(self)
        sizer.Add(self.canvas, pos=(1, 0), span=(0,11), flag=wx.EXPAND)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
        sizer.AddGrowableCol(10)
        sizer.AddGrowableRow(1)
        
        self.SetSizer(sizer)
        sizer.Fit(parent)
        
        
        
        
    def parametre(self, event):
        DialogParametre = Dialog_Parametre(self, self.canvas)
        DialogParametre.Show(True)
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    def play(self, event):
        if(self.canvas.tableauMap.shape != 0):
            if(self.entryAlgoBox.GetSelection() >= 0):
                self.boutonStop.Enable(True)
                self.boutonRePlay.Enable(True)
                self.boutonPlay.Enable(False)
                self.canvas.coordRobot = self.canvas.coordStartRobot
                AlgoBox = self.entryAlgoBox.GetString(self.entryAlgoBox.GetSelection())
                if(AlgoBox == "A* version 1"):
                    self.algo = AlgoAV1(self.canvas)
                if(AlgoBox == "A* version 2 - Pas de ligne droite"):
                    self.algo = AlgoAV2(self.canvas)
                if(AlgoBox == "A* version 3 - Pas de diagonale"):
                    self.algo = AlgoAV3(self.canvas) 
                if(AlgoBox == "A* version 4 - Problème de temps"):
                    self.algo = AlgoAV4(self.canvas)
                if(AlgoBox == "A* version 5 - Problème temps resolu"):
                    self.algo = AlgoAV5(self.canvas)
                if(AlgoBox == "A* version 6 - Pénalité"):
                    self.algo = AlgoAV6(self.canvas)
                if(AlgoBox == "A* version 7"):
                    self.algo = AlgoAV7(self.canvas)          
            else:
                Afficher("Vous devez sélèctionner un algorithme")
        else:
            Afficher("Vous devez lancer une simulation en générant un carte")
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()   
    def replay(self, event):
        self.stop(self)
        self.play(self)
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()     
    def stop(self, event):
        self.boutonStop.Enable(False)
        self.boutonRePlay.Enable(False)
        self.boutonPlay.Enable(True)
        self.algo.statut = 0
        self.canvas.AlgoCube = np.array([],'f')
        self.canvas.simulation = False
        self.canvas.afficherSolution = 2
        self.canvas.afficherAlgo = 2
        
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    def Start(self, event):
        
        
        self.canvas.coordRobot = [self.canvas.coordStartRobot[0], self.canvas.coordStartRobot[1]]
        
        
        self.view = RobotView(self.canvas)
        self.view.start()
        
        while self.view.statut != 2:
            pass
        self.commande = SerialInteract(self.canvas)
        if self.commande.statut == 1:
            self.commande.start()
            
            self.boutonStopRobot.Enable(True)
            self.boutonStart.Enable(False)
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    
    def stopRobot(self, event):    
        self.canvas.simulationReel = False
        while self.commande.statut == 2:
            pass
        self.view.statut = 0
        self.boutonStopRobot.Enable(False)
        self.boutonStart.Enable(True)
        
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    
    def NextStep(self, event):
        if self.canvas.simulation:    
            self.algo.nextTourAction()
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    def robotView(self, event):
        if self.canvas.simulation:  
            self.canvas.cameraPointCible = numpy.array([self.canvas.coordRobot[0],0.5,self.canvas.coordRobot[1]])
            self.canvas.cameraPosition = numpy.array([self.canvas.coordRobot[0]-1,0.5+3,self.canvas.coordRobot[1]-1])
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    def ShowSolution(self, event):
        if self.canvas.simulation:
            if self.algo.statut == 0:
                self.canvas.AlgoCube = np.array([],'f')
                self.canvas.AfficherAlgo = 0
                self.algo.start()
            elif self.algo.statut == 1:
                if self.canvas.afficherSolution == 1:
                    self.canvas.afficherSolution = 2
                elif self.canvas.afficherSolution == 2:
                    self.canvas.afficherSolution = 1
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    def DoSolution(self, event):
        
        if self.canvas.afficherAlgo == 2:
            self.canvas.afficherAlgo = 0
        if self.canvas.afficherAlgo == 1:
            self.canvas.afficherAlgo = 2
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
    def OnSize(self, event):
        self.canvas.SetSize(self.GetSize())
        event.Skip()
        size = self.canvas.size = self.canvas.GetClientSize()
        self.canvas.SetCurrent(self.canvas.context)
        glViewport(0, 0, size.width, size.height)
        #on defini le focus pour éviter que logiciel definisse le bouton comme le focus
        self.entryAlgoBox.SetFocus()
                           
class Frame_Principale(wx.Frame):
    def __init__(self):
        self.size = (int(config().FenetrePrincipaleLargeur), int(config().FenetrePrincipaleHauteur))
        wx.Frame.__init__(self, None, title=("Simulateur par Paul Capgras"), size = self.size)
        
        self.panel = PanelFrame_Principale(self)
        
        #Menu Principal
        statusMenuBarPrincipal = self.CreateStatusBar()
        menuBarPrincipal = MenuBar_Principale(self, self.panel.canvas)
        self.SetMenuBar(menuBarPrincipal)

class App_Principale(wx.App):
    def OnInit(self):
        framePrincipale = Frame_Principale()
        framePrincipale.Show(show=True)
        return True