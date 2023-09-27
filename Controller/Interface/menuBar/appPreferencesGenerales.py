# -*- coding: utf-8 -*-

#----------------------------------
import wx

#----------------------------------
from Usefull.fonctionsFichier import *
from Controller.Interface.AjouterUnParametre import *

#----------------------------------

class Dialog_PreferencesGenerales(wx.Dialog):
    def __init__(self, FramePrincipale, canvas):
        wx.Dialog.__init__(self, FramePrincipale)
        
        self.canvas = canvas
        
        def quitter(event):
            self.enregistrer()
            self.Destroy()
        def generer(event):
            self.enregistrer()
            self.Destroy()
            
        def cancel(event):
            self.Destroy()
            
        fontText10Gras = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.BOLD) 
        
        
        self.Title = "Préférences générales"
        self.Size = (400,400)
        
        panel = wx.Panel(self, 1, size=self.GetClientSize())
        
        textParametre = wx.StaticText(panel, 1, label="Paramètres:", pos=(6,6), style=wx.ST_ELLIPSIZE_END)
        textParametre.SetFont(fontText10Gras)
        self.Sensibilite = AjouterUnParametreList("Sensibilit", panel, textParametre.GetPosition(), textParametre.GetSize(), 0, (100,20), config().Sensibilite)
        self.Vitesse = AjouterUnParametreList("Vitesse de déplacement", panel, self.Sensibilite.position, self.Sensibilite.size, 0, (100,20), config().Vitesse)
        
        self.MurColor = AjouterUnParametreList("MurColor", panel, self.Vitesse.position, self.Vitesse.size, 0, (100,20), config().MurColor)
        self.MargeColor = AjouterUnParametreList("MargeColor", panel, self.MurColor.position, self.MurColor.size, 0, (100,20), config().MargeColor)
        
        self.SolutionColor = AjouterUnParametreList("SolutionColor", panel, self.MargeColor.position, self.MargeColor.size, 0, (100,20), config().SolutionColor)
        self.AlgoColor = AjouterUnParametreList("AlgoColor", panel, self.SolutionColor.position, self.SolutionColor.size, 0, (100,20), config().AlgoColor)
        

        Generer = wx.Button(panel, -1, "Sauvegarder")
        Generer.SetPosition((panel.GetSize()[0] - Generer.GetSize()[0]- 4, panel.GetSize()[1] - Generer.GetSize()[1]- 4))
        Generer.Bind(wx.EVT_BUTTON, quitter)
        
        Annuler = wx.Button(panel, -1, "Annuler")
        Annuler.SetPosition((4 , panel.GetSize()[1] - Annuler.GetSize()[1]-4))
        Annuler.Bind(wx.EVT_BUTTON, cancel)
        
        
        self.Bind(wx.EVT_CLOSE, quitter)
        
    def enregistrer(self):
        if (config().Sensibilite != self.Sensibilite.textEntry.GetValue()):
            config().editValue("Sensibilite", self.Sensibilite.textEntry.GetValue())
            self.canvas.sensibilite = int(self.Sensibilite.textEntry.GetValue())  
        if (config().Vitesse != self.Vitesse.textEntry.GetValue()):
            config().editValue("Vitesse", self.Vitesse.textEntry.GetValue())
            self.canvas.deplacement = eval(self.Vitesse.textEntry.GetValue())
        if (config().MurColor != self.MurColor.textEntry.GetValue()):
                config().editValue("MurColor", self.MurColor.textEntry.GetValue()) 
        if (config().MargeColor != self.MargeColor.textEntry.GetValue()):
                config().editValue("MargeColor", self.MargeColor.textEntry.GetValue()) 
        if (config().SolutionColor != self.SolutionColor.textEntry.GetValue()):
                config().editValue("SolutionColor", self.SolutionColor.textEntry.GetValue()) 
        if (config().AlgoColor != self.AlgoColor.textEntry.GetValue()):
                config().editValue("AlgoColor", self.AlgoColor.textEntry.GetValue()) 






