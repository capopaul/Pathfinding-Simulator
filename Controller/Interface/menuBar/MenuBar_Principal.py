# -*- coding: utf-8 -*-

#----------------------------------
import wx
import random
#----------------------------------
from Controller.Interface.menuBar.appParametreRealite import *
from Controller.Interface.menuBar.appLabyrinthe import *
from Controller.Interface.menuBar.appPreferencesGenerales import *
from Controller.Interface.menuBar.appParametreGeneraux import *
from View.Draw.AfficherMap import *
from Usefull.fonctionsFichier import *
from Usefull.afficher import *
from Model.extendMap import *
from Model.extendLab import *
from Model.marges import *

#----------------------------------

class MenuBar_Principale(wx.MenuBar):
    def __init__(self, FramePrincipale, canvas):
        wx.MenuBar.__init__(self)
        def openPreferencesGenerales(event):
            DialogPreferencesGenerales = Dialog_PreferencesGenerales(FramePrincipale, canvas)
            DialogPreferencesGenerales.Show(True)
            
        def openLabyrintheFenetre(event):
            DialogLabyrinthe = Dialog_Labyrinthe(FramePrincipale, canvas)
            DialogLabyrinthe.Show(True)
        
        def quitter(event):
            FramePrincipale.Close()
            
        def openParametreGeneraux(event):  
            DialogParametreGeneraux = Dialog_ParametreGeneraux(FramePrincipale)
            DialogParametreGeneraux.Show(True)
            
        def openParametreRealite(event):  
            DialogParametreRealite = Dialog_ParametreRealite(FramePrincipale)
            DialogParametreRealite.Show(True)     
             
        def quitterToutesSimulation(event):
            canvas.tableauMap = 0
            canvas.afficherMap = False    
        
        def ouvrirScene(event):
            openFileDialog = wx.FileDialog(FramePrincipale, "Ouvrir", "", "", 
                                      "Fichier texte (*.txt)|*.txt", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            print(openFileDialog.GetPath())
            try:
                fichier = open(openFileDialog.GetPath(), "r")
                lignesFichier = fichier.read().split(" \n")
                canvas.tableauMap = np.array([list(map(float, lignesFichier[n].split(" "))) for n in range(len(lignesFichier)-1)])
                afficher_map(canvas)
                canvas.matSimulation = np.array([],'f')
                fichier.close()
            except IOError:
                Afficher("Nous ne pouvons pas lire dans le lien:"+openFileDialog.GetPath())
            openFileDialog.Destroy()
            
        def enregistrerScene(event):
            saveFileDialog = wx.FileDialog(self, "Sauvegarder la scène actuelle", wildcard="txt files (*.txt)|*.txt",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            if saveFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            pathname = saveFileDialog.GetPath()
            try:
                fichier = open(pathname, "w")
                for z in range(len(canvas.tableauMap)):
                    for x in range(len(canvas.tableauMap[0])):
                        fichier.write(str(canvas.tableauMap[z][x])+" ")
                    fichier.write("\n")
                fichier.close()
                saveFileDialog.Destroy()
            except IOError:
                Afficher("Nous ne pouvons pas écrire dans le lien:"+pathname)
                
        def enleverMurs(event):
            extrusion = int(config().Extrusion)
            for x in range(len(canvas.tableauMap)):
                for z in range(len(canvas.tableauMap[0])):
                    if canvas.tableauMap[x][z] == 1:
                        if(int(100*random.random()+1) <= extrusion):
                            canvas.tableauMap[x][z] = 0
            afficher_map(canvas)
        
        def resetSimulation(event):
            canvas.matSimulation = np.array([],'f')
            canvas.afficherSolution = 2
            
        def extendLabEvent(event):
            ExtendLab(canvas)
            
        def extendMapEvent(event):
            ExtendMap(canvas)
            
        def margesEvent(event):
            Marges(canvas)
        def resetMargesEvent(event):
            ResetMarges(canvas)
        """
                A SUPPRRRRRIMMMMMERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
        """
        fichier = open("Saves/map/map vierge.txt", "r")
        lignesFichier = fichier.read().split(" \n")
        canvas.tableauMap = np.array([list(map(int, lignesFichier[n].split(" "))) for n in range(len(lignesFichier)-1)])
        afficher_map(canvas)
        fichier.close()
        
        """
        -------------------------------------------------------------------------------------------------------------------------
        """
        
        #Menu Fichier
        menuFichier = wx.Menu()
        
        fermerSimulation = menuFichier.Append(-1, 'Nouvelle Scene', 'Fermer la simulation en cours')
        self.Bind(wx.EVT_MENU, quitterToutesSimulation, fermerSimulation)
        
        ouvrir = menuFichier.Append(-1, 'Ouvrir...', 'Ouvre une scène qui a été enregistrée')
        self.Bind(wx.EVT_MENU, ouvrirScene, ouvrir)
        
        enregistrer = menuFichier.Append(-1, 'Enregistrer...', 'Enregistrer la scène actuelle pour pouvoir la réouvrir')
        self.Bind(wx.EVT_MENU, enregistrerScene, enregistrer)
        
        BoutonQuitter = menuFichier.Append(-1, "Quitter\tCtrl-Q", "Quitter la simulation")
        self.Bind(wx.EVT_MENU, quitter, BoutonQuitter)
        
        self.Append(menuFichier, "&Fichier")
        
        
         #Menu Simulations
        menuSimulation = wx.Menu()
        
        genererLabButton = menuSimulation.Append(-1, 'Générer un labyrinthe', 'Générer un labyrinthe')
        self.Bind(wx.EVT_MENU, openLabyrintheFenetre, genererLabButton)
        
        enleverMursButton = menuSimulation.Append(-1, 'Retirer des Murs Aléatoirement', 'Retirer des Murs Aléatoirement')
        self.Bind(wx.EVT_MENU, enleverMurs, enleverMursButton)
        
        extendMapButton = menuSimulation.Append(-1, 'Etendre la map', 'étendre la map')
        self.Bind(wx.EVT_MENU, extendMapEvent, extendMapButton)
        
        extendLabButton = menuSimulation.Append(-1, 'Etendre labyrinthe', 'étendre labyrinthe')
        self.Bind(wx.EVT_MENU, extendLabEvent, extendLabButton)
        
        margesButton = menuSimulation.Append(-1, 'Definir des marges', 'Definir des marges')
        self.Bind(wx.EVT_MENU, margesEvent, margesButton)
        
        resetMargesButton = menuSimulation.Append(-1, 'Reset des marges', 'Reset des marges')
        self.Bind(wx.EVT_MENU, resetMargesEvent, resetMargesButton)
        
        ResetSimulation = menuSimulation.Append(-1, 'Reset la simulation', 'Reset la simulation')
        self.Bind(wx.EVT_MENU, resetSimulation, ResetSimulation)
        
        quitterSimulation = menuSimulation.Append(-1, 'Fermer la simulation', 'Fermer la simulation')
        self.Bind(wx.EVT_MENU, quitterToutesSimulation, quitterSimulation)
        
        self.Append(menuSimulation, '&Simulation')
        
        
        #Menu Parametre
        menuParametre = wx.Menu()
        
        ParGeneraux = menuParametre.Append(-1, 'Généraux', 'Ouvre les paramètres généraux')
        self.Bind(wx.EVT_MENU, openParametreGeneraux,ParGeneraux)
        
        ParRealite = menuParametre.Append(-1, 'Réalité', 'Ouvre les paramètres de la réalité')
        self.Bind(wx.EVT_MENU, openParametreRealite,ParRealite)
        
        self.Append(menuParametre, '&Paramètres')
        
        
        #Menu Preference
        menuPreference = wx.Menu()
        
        PreferencesGenerales = menuPreference.Append(-1, 'Préférence générales', 'Ouvre les préférences globales')
        self.Bind(wx.EVT_MENU, openPreferencesGenerales, PreferencesGenerales)
        
        self.Append(menuPreference, '&Préférence')