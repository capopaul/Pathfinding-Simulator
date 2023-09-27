# -*- coding: utf-8 -*-

#----------------------------------
import wx

#----------------------------------

#----------------------------------

class Afficher():
    def __init__(self, message):
         wx.MessageBox(message, 'Informations:', wx.OK | wx.ICON_INFORMATION)
        