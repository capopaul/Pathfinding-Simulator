#----------------------
from OpenGL.GL import *
from numpy import *

#----------------------
from Usefull.fonctionsFichier import *
from View.objects.cube import *
#----------------------

def wall(canvas, LargeurX, LongueurZ): 
    ySize = int(config().ReturnValue("HauteurMur"))+0.5
    color = list(map(float, config().ReturnValue('MurColor').split(",")))
    
    canvas.indexObjects = np.append(canvas.indexObjects, arrayIndexCube(len(canvas.vertexObjects)/6))
    canvas.vertexObjects = np.append(canvas.vertexObjects, arrayVertCube(pos1=(-1, 0, -1),
                                                                         pos2=(LargeurX+1, ySize, 0),
                                                                         color = [*color]))
    
    canvas.indexObjects = np.append(canvas.indexObjects, arrayIndexCube(len(canvas.vertexObjects)/6))
    canvas.vertexObjects = np.append(canvas.vertexObjects, arrayVertCube(pos1=(-1, 0, 0),
                                                                         pos2=(0, ySize, LongueurZ+1),
                                                                         color = [*color]))
    
    canvas.indexObjects = np.append(canvas.indexObjects, arrayIndexCube(len(canvas.vertexObjects)/6))
    canvas.vertexObjects = np.append(canvas.vertexObjects, arrayVertCube(pos1=(0, 0, LongueurZ),
                                                                         pos2=(LargeurX+1, ySize, LongueurZ+1),
                                                                         color = [*color]))
    
    canvas.indexObjects = np.append(canvas.indexObjects, arrayIndexCube(len(canvas.vertexObjects)/6))
    canvas.vertexObjects = np.append(canvas.vertexObjects, arrayVertCube(pos1=(LargeurX, 0, 0),
                                                                         pos2=(LargeurX+1, ySize, LongueurZ),
                                                                         color = [*color]))
    
def repere(longueur):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(-1, 0, -1)
    glBegin(GL_LINES)
    glColor3ub(0,0,140)
    glVertex3d(0,0,0)
    glVertex3d(longueur,0,0)
    
    glColor3ub(200,0,0)
    glVertex3d(0,0,0)
    glVertex3d(0,longueur,0)
    
    glColor3ub(0 ,200 , 0)
    glVertex3d(0,0,0)
    glVertex3d(0,0,longueur)
    glEnd()
    glLoadIdentity()