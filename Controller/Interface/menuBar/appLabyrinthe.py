# -*- coding: utf-8 -*-

#----------------------------------
import wx
#----------------------------------
from Usefull.fonctionsFichier import *
from Controller.Interface.AjouterUnParametre import *
from Model.genererLabyrinthe import generer_labyrinthe
from View.Draw.AfficherMap import *

#----------------------------------
        
class Dialog_Labyrinthe(wx.Dialog):
    def __init__(self, FramePrincipale, canvas):
        wx.Dialog.__init__(self, FramePrincipale)
        def quitter(event):
            self.enregistrer()
            self.Destroy()
        def generer(event):
            self.enregistrer()
            self.Destroy()
            canvas.tableauMap = generer_labyrinthe(canvas)
            canvas.matSimulation = np.array([],'f')
            afficher_map(canvas)
            canvas.matSimulation = np.array([])
            
        def cancel(event):
            self.Destroy()
            
        fontText10Gras = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.BOLD) 
        
        
        self.Title = "Générer un labyrinthe"
        self.Size = (400,400)
        
        panel = wx.Panel(self, 1, size=self.GetClientSize())
        
        textLabyrinthe = wx.StaticText(panel, 1, label="Paramètre de la génération", pos=(6,6), style=wx.ST_ELLIPSIZE_END)
        textLabyrinthe.SetFont(fontText10Gras)
        self.LargeurLab = AjouterUnParametreSpinner("LargeurLab", panel, textLabyrinthe.GetPosition(), textLabyrinthe.GetSize(), 0, (80,20), 0, 1000, int(config().LargeurLab))
        self.HauteurLab = AjouterUnParametreSpinner("HauteurLab", panel, self.LargeurLab.position, self.LargeurLab.size, 0, (80,20), 0, 1000,int(config().HauteurLab))
        
        Generer = wx.Button(panel, -1, "Générer")
        Generer.SetPosition((panel.GetSize()[0] - Generer.GetSize()[0]- 4, panel.GetSize()[1] - Generer.GetSize()[1]- 4))
        Generer.Bind(wx.EVT_BUTTON, generer)
        
        Annuler = wx.Button(panel, -1, "Annuler")
        Annuler.SetPosition((4 , panel.GetSize()[1] - Annuler.GetSize()[1]-4))
        Annuler.Bind(wx.EVT_BUTTON, cancel)
        
        
        self.Bind(wx.EVT_CLOSE, quitter)
        
    def enregistrer(self):
            if self.LargeurLab.spinner.GetValue() <= 10000 and int(config().LargeurLab) != self.LargeurLab.spinner.GetValue():    
                config().editValue("LargeurLab", str(self.LargeurLab.spinner.GetValue()))  
            if self.HauteurLab.spinner.GetValue() <= 10000 and int(config().HauteurLab) != self.HauteurLab.spinner.GetValue():    
                config().editValue("HauteurLab", str(self.HauteurLab.spinner.GetValue()))
            