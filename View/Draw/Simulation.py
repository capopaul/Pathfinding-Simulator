#----------------------------------
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#----------------------------------

#----------------------------------

def simulation(canvas):
    rayon = canvas.tailleRobot/2
    
    glu = gluNewQuadric()
    
    gluQuadricDrawStyle(glu,GLU_LINE);
    
    glTranslated(canvas.coordRobot[0]+0.5, rayon, canvas.coordRobot[1]+0.5)
    gluSphere(glu, rayon, 50, 50)
    
    gluDeleteQuadric(glu)
    