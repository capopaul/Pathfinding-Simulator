# -*- coding: utf-8 -*-

#----------------------------------
import wx
#----------------------------------
from Usefull.fonctionsFichier import *
from Controller.Interface.AjouterUnParametre import *

#----------------------------------
class Dialog_ParametreGeneraux(wx.Dialog):
    def __init__(self, FramePrincipale):
        wx.Dialog.__init__(self, FramePrincipale)
        def sauvegarder():
            if (Extrusion.spinner.GetValue() <= 10000 and int(config().FenetrePrincipaleHauteur) != Extrusion.spinner.GetValue()):
                config().editValue("Extrusion", str(Extrusion.spinner.GetValue()))
            if (HauteurMur.spinner.GetValue() <= 10000 and int(config().HauteurMur) != HauteurMur.spinner.GetValue()):
                config().editValue("HauteurMur", str(HauteurMur.spinner.GetValue()))
            if (LargeurMur.spinner.GetValue() <= 10000 and int(config().LargeurMur) != LargeurMur.spinner.GetValue()):
                config().editValue("LargeurMur", str(LargeurMur.spinner.GetValue()))
            if (LongueurCase.spinner.GetValue() <= 10000 and int(config().LongueurCase) != LongueurCase.spinner.GetValue()):
                config().editValue("LongueurCase", str(LongueurCase.spinner.GetValue()))
            if (LargeurCase.spinner.GetValue() <= 10000 and int(config().LargeurCase) != LargeurCase.spinner.GetValue()):
                config().editValue("LargeurCase", str(LargeurCase.spinner.GetValue()))
        def cancel(event):
            self.Destroy()
        def quitter(event):
            sauvegarder() 
            self.Destroy()
        fontText10Gras = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.BOLD) 
         
        self.Title = "Paramètres généreaux"
        self.Size = (400,400)
        panel = wx.Panel(self, 1, size=self.GetClientSize())   
        textParametre = wx.StaticText(panel, 1 ,"Listes des paramètres généraux:", pos=(6,6), style=wx.ST_ELLIPSIZE_END)
        textParametre.SetFont(fontText10Gras)
        Extrusion = AjouterUnParametreSpinner("Extrusion", panel, textParametre.GetPosition(), textParametre.GetSize(), 4, 
                                               (80,20), 0, 100, int(config().Extrusion))
        HauteurMur = AjouterUnParametreSpinner("HauteurMur", panel, Extrusion.position, Extrusion.size, 4, 
                                               (80,20), 0, 1000, int(config().HauteurMur))
        LargeurMur = AjouterUnParametreSpinner("LargeurMur", panel, HauteurMur.position, HauteurMur.size, 4, 
                                               (80,20), 0, 100, int(config().LargeurMur))
        LongueurCase = AjouterUnParametreSpinner("LongueurCase", panel, LargeurMur.position, LargeurMur.size, 4, 
                                               (80,20), 0, 100, int(config().LongueurCase))
        LargeurCase = AjouterUnParametreSpinner("LargeurCase", panel, LongueurCase.position, LongueurCase.size, 4, 
                                               (80,20), 0, 100, int(config().LargeurCase))
        
        
        Generer = wx.Button(panel, -1, "Sauvegarder")
        Generer.SetPosition((panel.GetSize()[0] - Generer.GetSize()[0]- 4, panel.GetSize()[1] - Generer.GetSize()[1]- 4))
        Generer.Bind(wx.EVT_BUTTON, quitter)
        
        Annuler = wx.Button(panel, -1, "Annuler")
        Annuler.SetPosition((4 , panel.GetSize()[1] - Annuler.GetSize()[1]-4))
        Annuler.Bind(wx.EVT_BUTTON, cancel)
        
        self.Bind(wx.EVT_CLOSE, quitter)
        
            
        
        
            