# -*- coding: utf-8 -*-

#----------------------------------
import wx
#----------------------------------
from Controller.Interface.AjouterUnParametre import *
from Usefull.afficher import *
from Model.usefull import *

#----------------------------------

class Dialog_Parametre(wx.Dialog):
    def __init__(self, FramePrincipale, canvas):
        wx.Dialog.__init__(self, FramePrincipale)
        
        def sauvegarder():
            try:
                if ((canvas.tableauMap[int(departZ.textEntry.GetValue()), int(departX.textEntry.GetValue())] != 1 
                    and canvas.tableauMap[int(departZ.textEntry.GetValue()), int(departX.textEntry.GetValue())] != 2)
                    and (canvas.tableauMap[int(finZ.textEntry.GetValue()), int(finX.textEntry.GetValue())] != 1
                    and canvas.tableauMap[int(finZ.textEntry.GetValue()), int(finX.textEntry.GetValue())] != 1 )):
                    
                    coordStartRobot(canvas,[int(departX.textEntry.GetValue()), int(departZ.textEntry.GetValue())])  
                    coordEndRobot(canvas, [int(finX.textEntry.GetValue()), int(finZ.textEntry.GetValue())])  
                    canvas.tailleRobot = int(robotTaille.textEntry.GetValue())
                     
                    canvas.actualiser = True
                    return True
                else:
                    Afficher("Erreur veuillez configurer le point de départ et d arrivée")
            except ValueError:
                Afficher("Erreur vous devez rentrer des nombres")
        def cancel(event):
            self.Destroy()
        def quitter(event):
            if sauvegarder():        
                self.Destroy()
        
        fontText10Gras = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.BOLD) 
        
        
        self.Title = "Paramètre de l'algorithme"
        self.Size = (400,400)
        
        panel = wx.Panel(self, 1, size=self.GetClientSize())
        
        textLabyrinthe = wx.StaticText(panel, 1 ,label="Listes des paramètres de l'algorithme:", pos=(6,6), style=wx.ST_ELLIPSIZE_END)
        textLabyrinthe.SetFont(fontText10Gras)
        
        departX = AjouterUnParametreList("Coordonnée de Départ X", panel, textLabyrinthe.GetPosition(), textLabyrinthe.GetSize(), 0, (100,20), str(canvas.coordStartRobot[0]))
        departZ = AjouterUnParametreList("Coordonnée de Départ Z", panel, departX.position, departX.size, 0, (100,20), str(canvas.coordStartRobot[1]))
        finX = AjouterUnParametreList("Coordonnée d'arrivée X", panel, departZ.position, departZ.size, 0, (100,20), str(canvas.coordEndRobot[0]))
        finZ = AjouterUnParametreList("Coordonnée d'arrivée Z", panel, finX.position, finX.size, 0, (100,20), str(canvas.coordEndRobot[1]))
        robotTaille = AjouterUnParametreList("Taille du robot (nombre impair de preference)", panel, finZ.position, finZ.size, 0, (100,20), str(canvas.tailleRobot))
        
        Generer = wx.Button(panel, -1, "Sauvegarder")
        Generer.SetPosition((panel.GetSize()[0] - Generer.GetSize()[0]- 4, panel.GetSize()[1] - Generer.GetSize()[1]- 4))
        Generer.Bind(wx.EVT_BUTTON, quitter)
        
        Annuler = wx.Button(panel, -1, "Annuler")
        Annuler.SetPosition((4 , panel.GetSize()[1] - Annuler.GetSize()[1]-4))
        Annuler.Bind(wx.EVT_BUTTON, cancel)
        
        self.Bind(wx.EVT_CLOSE, quitter)