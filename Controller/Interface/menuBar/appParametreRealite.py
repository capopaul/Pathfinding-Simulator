# -*- coding: utf-8 -*-

#----------------------------------
import wx
#----------------------------------
from Usefull.fonctionsFichier import *
from Controller.Interface.AjouterUnParametre import *

#----------------------------------
class Dialog_ParametreRealite(wx.Dialog):
    def __init__(self, FramePrincipale):
        wx.Dialog.__init__(self, FramePrincipale)
        def sauvegarder():
            if (config().Reel_Echelle != Echelle.textEntry.GetValue()):
                config().editValue("Reel_Echelle", Echelle.textEntry.GetValue())
            if (config().CoeffRotation != CoeffRotation.textEntry.GetValue()):
                config().editValue("CoeffRotation", CoeffRotation.textEntry.GetValue())
            if (config().EchelleRelleCamera != EchelleRelleCamera.textEntry.GetValue()):
                config().editValue("EchelleRelleCamera", EchelleRelleCamera.textEntry.GetValue())    
            if (config().Port != Port.textEntry.GetValue()):
                config().editValue("Port", Port.textEntry.GetValue())
            if (config().DistanceChangePoint != DistanceChangePoint.textEntry.GetValue()):
                config().editValue("DistanceChangePoint", DistanceChangePoint.textEntry.GetValue())       
        def cancel(event):
            self.Destroy()
        def quitter(event):
            sauvegarder() 
            self.Destroy()
        fontText10Gras = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.BOLD) 
         
        self.Title = "Paramètre du robot"
        self.Size = (400,400)
        panel = wx.Panel(self, 1, size=self.GetClientSize()) 
          
        textParametre = wx.StaticText(panel, 1 ,"Listes des paramètres du robot dans la réalité: ", pos=(6,6), style=wx.ST_ELLIPSIZE_END)
        textParametre.SetFont(fontText10Gras)
        Port = AjouterUnParametreList("Port: ", panel, textParametre.GetPosition(), textParametre.GetSize(), 0,
                                               (80,20), config().Port)
        Echelle = AjouterUnParametreList("Echelle: ", panel, Port.position, Port.size, 0,
                                               (80,20), config().Reel_Echelle)
        EchelleRelleCamera = AjouterUnParametreList("EchelleRelleCamera: ", panel, Echelle.position, Echelle.size, 0,
                                               (80,20), config().EchelleRelleCamera)
        CoeffRotation = AjouterUnParametreList("Coefficient de rotation: ", panel, EchelleRelleCamera.position, EchelleRelleCamera.size, 0,
                                               (80,20), config().CoeffRotation)
        DistanceChangePoint = AjouterUnParametreList("DistanceChangePoint: ", panel, CoeffRotation.position, CoeffRotation.size, 0,
                                               (80,20), config().DistanceChangePoint)
        
        
        
        Generer = wx.Button(panel, -1, "Sauvegarder")
        Generer.SetPosition((panel.GetSize()[0] - Generer.GetSize()[0]- 4, panel.GetSize()[1] - Generer.GetSize()[1]- 4))
        Generer.Bind(wx.EVT_BUTTON, quitter)
        
        Annuler = wx.Button(panel, -1, "Annuler")
        Annuler.SetPosition((4 , panel.GetSize()[1] - Annuler.GetSize()[1]-4))
        Annuler.Bind(wx.EVT_BUTTON, cancel)
        
        self.Bind(wx.EVT_CLOSE, quitter)
        
            
        
        
            