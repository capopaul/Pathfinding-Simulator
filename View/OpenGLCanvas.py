#----------------------------------
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

#----------------------------------
from Controller.eventManager import *
from update import *

#----------------------------------
class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, panel):      
        
        glcanvas.GLCanvas.__init__(self, panel, -1, size=(800,800))
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        
        #Active la profondeur
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.1, 0, 0.3, 1) #Couleur de l'environnement
        
        self._attributExterne()
        self._attributInterne()
        
        #Boucle principale du programme
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._appelUpdate)
        self._timer.Start(25)
        
        self.next = True
        
    def _attributExterne(self):
        def _modele():
            #Info du robot
            self.tailleRobot = 1
            self.coordStartRobot = [0, 0]
            self.coordEndRobot = [6, 0]
            self.coordRobot = [self.coordStartRobot[0], self.coordStartRobot[1]]
            
            
            
            #Map de mani�re array
            self.tableauMap = 0
            
            #Liste des deplacements du robot lors de la solution
            self.vecteurSolution = []
            self.pointSolution =np.array([])
            
            
            #Variable globale Robot en temps r�al
            
            
        def _view():
            def _camera():
                #Parametres de deplacement
                self.sensibilite = int(config().ReturnValue("Sensibilite"))
                self.deplacement = eval(config().ReturnValue("Vitesse"))
                
                #Les trois parametres de la camera
                self.cameraPosition = numpy.array([0.,3.,0.])
                self.cameraPointCible = numpy.array([1.,1.,1.])
                self.axeVertical = numpy.array([0.,1.,0.])
                
                #Matrice de d�placement Model* View*Projection
                self.loc_mvp = []   
            def _renderMurs():
                #Coordonn�e des cubes qui representent les murs    
                self.Mur = np.array([])
                self.indexMur = np.array([])
                self.shader_Wall = compile_shader("View/shaders/instance/vertex_shader", "View/shaders/instance/fragment_shader")
                self.VAOMur = 0
            def _renderMarges():
                #Coordonn�e des cubes qui representent les murs    
                self.Marge = np.array([])
                self.indexMarge = np.array([])
                self.shader_Marge = compile_shader("View/shaders/instance/vertex_shader", "View/shaders/instance/fragment_shader")
                self.VAOMarge = 0
            def _renderObjects():
                self.vertexObjects = np.array([],'f')
                self.indexObjects = np.array([], dtype=np.uint32)
                self.shader_Objects = compile_shader("View/shaders/simple/vertex_shader", "View/shaders/simple/fragment_shader")
                self.VAOObjects = 0 
            def _renderSimulation():
                self.matSimulation = np.array([],'f')
                self.indexSimulation = np.array([], dtype=np.uint32)
                self.shader_Simulation = compile_shader("View/shaders/transformation/vertex_shader", "View/shaders/transformation/fragment_shader")
                self.VAOSimulation = 0
            def _renderEditMode(): 
                self.indexEditMode = np.array([], dtype=np.uint32)
                self.shader_EditMode = compile_shader("View/shaders/static/vertex_shader", "View/shaders/static/fragment_shader")
                self.VAOEditMode = 0
            def _renderAlgo():
                self.AlgoCube = np.array([],'f')
                self.AlgoCubeNewValue = np.array([],'f')
                self.nextAlgoCube = True
                self.indexAlgo = np.array([], dtype=np.uint32)
                self.shader_Algo = compile_shader("View/shaders/instance/vertex_shader", "View/shaders/instance/fragment_shader")
                self.VAOAlgo = 0
            def _renderLignes():
                self.coordLigne = np.array([], 'f')
                self.indexLignes = np.array([], dtype=np.uint32)
                self.shader_Lignes = compile_shader("View/shaders/instance/vertex_shader", "View/shaders/instance/fragment_shader")
                self.VAOLignes = 0
                  
            _camera()
            _renderMurs()
            _renderMarges()
            _renderObjects()
            _renderSimulation()
            _renderEditMode()
            _renderAlgo()
            _renderLignes()
            
        def _controlleur():
            self.simulationReel = False
            #Une simulation est active
            self.simulation = False    
            
            #Afficher une map    
            self.afficherMap = False
            
            #Afficher marge
            self.afficherMarge = False
            
            #Afficher la solution
            self.afficherSolution = 2
            
            self.afficherAlgo = 2
            
            self.actualiser = False
            
            self.editMode = False
            
            self.ligneMode = True
        def _realite():    
            self.ligneDetectee = False
            
        _modele()
        _view()
        _controlleur()
        _realite()
        
    def _attributInterne(self):    
        self._orientation = numpy.array(self.cameraPointCible-self.cameraPosition)
        self._theta = 0
        self._phi = 0
        self._deplacementLateral = numpy.array([0.,0.,0.])
        self._memoMousePosition = numpy.array([0,0])
        
    #Fonction qui appelle la boucle principale du programme    
    def _appelUpdate(self, evt):
        update(self)
        