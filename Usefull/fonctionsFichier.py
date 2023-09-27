# -*- coding: utf-8 -*-

#----------------------------------

#----------------------------------

#----------------------------------

class config():
    def __init__(self):
            
        self.FenetrePrincipaleLargeur = self.ReturnValue("FenetrePrincipaleLargeur")
        self.FenetrePrincipaleHauteur = self.ReturnValue("FenetrePrincipaleHauteur")
        self.HauteurMur = self.ReturnValue("HauteurMur")
        self.LongueurCase = self.ReturnValue("LongueurCase")
        self.LargeurCase = self.ReturnValue("LargeurCase")
        self.LargeurMur = self.ReturnValue("LargeurMur")
        self.MurColor = self.ReturnValue("MurColor")
        self.MargeColor = self.ReturnValue("MargeColor")
        self.SolutionColor = self.ReturnValue("SolutionColor")
        self.AlgoColor = self.ReturnValue("AlgoColor")
        self.LargeurLab = self.ReturnValue("LargeurLab")
        self.HauteurLab = self.ReturnValue("HauteurLab")
        self.Vitesse = self.ReturnValue("Vitesse")
        self.Sensibilite = self.ReturnValue("Sensibilite")
        self.Extrusion = self.ReturnValue("Extrusion")
        self.Port = self.ReturnValue("Port")
        self.Reel_Echelle = self.ReturnValue("Reel_Echelle")
        self.EchelleRelleCamera = self.ReturnValue("EchelleRelleCamera")
        self.CoeffRotation = self.ReturnValue("CoeffRotation")
        self.DistanceChangePoint = self.ReturnValue("DistanceChangePoint")
        
        
    def ReturnValue(self, nom):
        try:
            fichier = open("saves/config.txt", "r")
            lignes = fichier.read().split("\n")
            fichier.close()
            for i in range(len(lignes)):
                if lignes[i].find(nom+": ") != -1:
                    return lignes[i].replace(nom+": ","")
            return -1
        except FileNotFoundError:
            self.__creerConfig()
            return -1
    
    def editValue(self, nom, newValue):  
        try:
            fichier = open("saves/config.txt", "r")
            lignes = fichier.read().split("\n")
            fichier.close()
            for i in range(len(lignes)):
                if lignes[i].find(nom+": ") != -1:
                    lignes[i] = lignes[i].replace(lignes[i], nom + ": " + newValue)
                    self.__editConfig(lignes)
                    break
        except FileNotFoundError:
            self.__creerConfig()
    
    def __editConfig(self, lignes):
        try:
            fichier = open("saves/config.txt", "w")
            for i in range(len(lignes)):
                fichier.write(lignes[i]+"\n")
            fichier.close()
        except FileNotFoundError:
            self.__creerConfig()
    def __creerConfig(self):
        fichier = open("saves/config.txt", "w")
        fichier.write("FenetrePrincipaleLargeur: 800\n")
        fichier.write("FenetrePrincipaleHauteur: 800\n")
        fichier.write("HauteurMur: 1\n")
        fichier.write("LargeurMur: 1\n")
        fichier.write("LongueurCase: 1\n")
        fichier.write("LargeurCase: 1\n")
        fichier.write("MurColor: 1,0,0\n")
        fichier.write("MargeColor: 0.8,0.1,0.5\n")
        fichier.write("SolutionColor: 0,1,0\n")
        fichier.write("AlgoColor: 1,0.5,0.5\n")
        fichier.write("LargeurLab: 40\n")
        fichier.write("HauteurLab: 25\n")
        fichier.write("Vitesse: 0.3\n")
        fichier.write("Sensibilite: 1000\n")
        fichier.write("Extrusion: 5\n")
        fichier.write("Port: COM7")
        fichier.write("Reel_Echelle: 2\n")
        fichier.write("EchelleRelleCamera: 80\n")
        fichier.write("CoeffRotation: 2\n")
        fichier.write("DistanceChangePoint: 2\n")
        fichier.close()