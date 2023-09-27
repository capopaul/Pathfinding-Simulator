#----------------------------------
from OpenGL.GL import *
from OpenGL.GLU import *

#----------------------------------

#---------------------------------

def Camera(canvas):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70,canvas.GetSize()[0]/canvas.GetSize()[1], 0.1, 1000)
    gluLookAt(*canvas.cameraPosition,
             *canvas.cameraPointCible,
              *canvas.axeVertical)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
        