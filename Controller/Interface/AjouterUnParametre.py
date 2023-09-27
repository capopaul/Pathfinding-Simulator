# -*- coding: utf-8 -*-

#----------------------------------
import wx
#----------------------------------


#----------------------------------

class AjouterUnParametreSpinner:
    def __init__(self, nom, panel, refPosition, refSize, posx, sizeSpinner, minSpinner, maxSpinner, defaultValue):
        text = wx.StaticText(panel, -1, "- "+nom, pos=(refPosition[0] + posx,
                                                        refPosition[1] + refSize[1]*1.5 + 4))
        fontText10 = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.NORMAL)
        text.SetFont(fontText10)
        
        self.size = text.GetSize()
        self.position = text.GetPosition()
        
        self.spinner = wx.SpinCtrl(panel, -1, size=sizeSpinner, pos=(self.position[0] + self.size[0] + 20,
                                                             self.position[1]))
        self.spinner.SetRange(1, 10000)
        self.spinner.SetValue(defaultValue)
        
        
class AjouterUnParametreList:
    def __init__(self, nom, panel, refPosition, refSize, posx, sizeText, defaultText):
        text = wx.StaticText(panel, -1, "- "+nom, pos=(refPosition[0] + posx,
                                                        refPosition[1] + refSize[1]*1.5 + 4))
        fontText10 = wx.Font(10, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.NORMAL)
        text.SetFont(fontText10)
        
        self.size = text.GetSize()
        self.position = text.GetPosition() 
        
        self.textEntry = wx.TextCtrl(panel, -1, defaultText, size=sizeText, pos=(self.position[0] + self.size[0] + 20,
                                                             self.position[1]))