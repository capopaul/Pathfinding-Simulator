# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math as mp
from threading import Thread

from Usefull.fonctionsFichier import *

class RobotView(Thread):
    def __init__(self, canvas):
        Thread.__init__(self)
        # -1: erreur initialisation : 0: valeur au depart: 1 = initialisation faite avec succès ; 2 traitement en cours thread lancé; 3 : fini
        self.statut = 1
        self.canvas=  canvas
    
    def run(self):
        ECHELLE = float(config().EchelleRelleCamera)
        cap = cv2.VideoCapture(1)
    
        def nothing(x):
            pass
        
        IMAGE_H = 480
        IMAGE_W = 640
        
        Distord = 60
        
        
        MULT = 2
        #Fixed at two  
        
        src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W, 0]])
        dst = np.float32([[ (IMAGE_W/2-Distord )*MULT , IMAGE_H*MULT], [(IMAGE_W/2+Distord)*MULT, IMAGE_H*MULT], [0, 0], [IMAGE_W*MULT, 0]])
        M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
        Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation
        
        kerneldenoise = (20,20)
        
        kerneldilate = np.ones((15,15),np.uint8)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        linelistmapx = np.empty([1,1])
        linelistmapy = np.empty([1,1])
        linelistmapa = np.empty([1,1])
        
        
        robotPos = [self.canvas.coordStartRobot[0]*(-ECHELLE),self.canvas.coordStartRobot[1]*(-ECHELLE)]
        robotAng = 90
        
        LineThreshold = 180
        
        cv2.namedWindow('mask')
        
        cv2.createTrackbar('lH','mask',0,360,nothing)
        cv2.createTrackbar('lS','mask',0,255,nothing)
        cv2.createTrackbar('lV','mask',0,255,nothing)
        cv2.createTrackbar('hH','mask',0,360,nothing)
        cv2.createTrackbar('hS','mask',0,255,nothing)
        cv2.createTrackbar('hV','mask',0,255,nothing)
        
        def globaltolocal(array):
        
            return [500+int(array[0]*Zoom),500+int(array[1]*Zoom)]
        
        self.statut = 2    
           
        while self.statut == 2:
            
            #initalise the global map for the robot
            Globalmap = np.zeros((1000,1000,3))
        
            Zoom = 0.1
        
        
            robotlocalPos = globaltolocal(robotPos)
        
            robotBox = cv2.boxPoints( ((robotlocalPos[0],robotlocalPos[1]),(60*Zoom,30*Zoom),robotAng) )
            robotBox = np.int0(robotBox)
            cv2.drawContours(Globalmap,[robotBox],0,(0,0,255),2)
        
            #fin
            
            ret,frame = cap.read()
        
            frame = cv2.convertScaleAbs(frame, alpha=1, beta=0) #contraste et lumino
            img = frame[0:(0+IMAGE_H), 0:IMAGE_W] # Apply np slicing for ROI crop
        
        
            
            warped_img = cv2.warpPerspective(img, M, (IMAGE_W*MULT, IMAGE_H*MULT)) # Image warping
            warpedshape = warped_img.shape
        
            rows,cols = warped_img.shape[:2]
        
            
            whiteimg = np.zeros(warped_img.shape)
            
            
            
            hsv = cv2.cvtColor(warped_img, cv2.COLOR_BGR2HSV)
        
            # define range of blue color in HSV
            lH =  cv2.getTrackbarPos('lH','mask')
            lS =  cv2.getTrackbarPos('lS','mask')
            lV =  cv2.getTrackbarPos('lV','mask')
        
            hH =  cv2.getTrackbarPos('hH','mask')
            hS =  cv2.getTrackbarPos('hS','mask')
            hV =  cv2.getTrackbarPos('hV','mask')
            
            lower_green = np.array([lH,lS,lV])
            upper_green = np.array([hH,hS,hV])
            
            lower_green = np.array([0,60,207])
            upper_green = np.array([22,255,255])
            
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_green, upper_green)
            denoise = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kerneldenoise )
            #---------------
            
            denoise = cv2.dilate(mask,kerneldilate,iterations = 1)
            #ret3,threshold2 = cv2.threshold(threshold,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
            
                
            cnts, hierarchy = cv2.findContours(denoise, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            
            linelist = np.array([[0,0,0]])
        
            #Triger rectangle remplace break
        
            index = 0
        
            
            
            for c in cnts:
        
                index +=1
        
                cv2.drawContours(whiteimg,[c],0,(120,120,120),2)
                
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
                cv2.drawContours(whiteimg,[approx],0,(0,0,120),2)
                
                moments = cv2.moments(c)
                Area = moments['m00']
        
                ((x,y),(w,h),t) = cv2.minAreaRect(approx)
                
                # if the contour has four vertices, then we have found
                # the thermostat display
                if  Area > 5000 and Area < 10**5 and (w<500 and h<500) and (w>h*1.5 or h>w*1.5):
                    
                        box = cv2.boxPoints( ((x,y),(w,h),t) )
                        box = np.int0(box)
        
                        [vx,vy,x,y] = cv2.fitLine(approx, cv2.DIST_L2,0,0.01,0.01)
                        if(vy<0 and vy>vx):
                            vy= vy*-1
                            vx=vx*-1
        
                        if(vx<0 and vx>vy):
                            vy= vy*-1
                            vx=vx*-1
                         
                        cv2.line(whiteimg,(x-vx*100,y-vy*100),(x+vx*50,y+vy*50),(0,255,0),2)
        
                       
                        
                        angle = np.angle([complex(vx,vy)],deg=False ) 
                        
                        
                        cv2.putText(whiteimg,str(int(mp.degrees(angle)))+"D "+str(index),(int(x),int(y)), font, 2,(255,255,255),2,cv2.LINE_AA)
            
                        cv2.drawContours(whiteimg,[box],0,(0,0,255),2)
                        
                        linelist= np.append(linelist,[[float( (warpedshape[1]/2)-x),float(warpedshape[0]-y),float(angle)]],axis=0)
        
            #traitement des lignes
        
            linelist = np.delete(linelist,0,0)
                
            s = mp.sin( mp.radians( robotAng) )
            c = mp.cos( mp.radians( robotAng) )
        
            diffx=0
            diffy=0
            diffa = 0
        
            
            
            if(len(linelist)>0):
                
                for line in linelist :
        
                    
                    linex= (line[0]*c - line[1]*s) + robotPos[0]
                    liney = (line[0]*s + line[1]*c) + robotPos[1]
        
                    linePos = np.array([linex,liney])
                    linelocalPos= globaltolocal(linePos)
        
                    anglevx = float ( mp.cos(line[2]+mp.radians( robotAng) ) ) *Zoom*60
                    anglevy = float ( mp.sin(line[2]+mp.radians(robotAng)) ) *Zoom*60
                    
                    cv2.line(Globalmap,(linelocalPos[0]-int(anglevx),linelocalPos[1]-int(anglevy)),(linelocalPos[0]+int(anglevx),linelocalPos[1]+int(anglevy)),(0,100,0),2)
        
                    X = np.sqrt( np.square( linelistmapx - linex ) +  np.square( linelistmapy - liney ) )
                    
                    idx = np.where( X == X.min() )
        
                    if(X[idx]>(LineThreshold)):
                    
                        linelistmapx = np.append(linelistmapx,linex)
                        linelistmapy = np.append(linelistmapy,liney)
                        linelistmapa = np.append(linelistmapa,line[2]+ mp.radians(robotAng) )
                    else :
                        diffx+=float((linelistmapx[idx]-linex)/len(linelist))
                        diffy+=float((linelistmapy[idx]-liney)/len(linelist))
                        diffa+=((linelistmapa[idx]-( line[2]+mp.radians(robotAng) ) ) )/len(linelist)
                        #print(((linelistmapa[idx]-( line[2]+mp.radians(robotAng) ) ) )/len(linelist))
                        
            
            robotPos[0] += diffx
            robotPos[1] += diffy
            print(robotPos)
            self.canvas.coordRobot = [(-1)*float(robotPos[0])/ECHELLE, (-1)*float(robotPos[1])/ECHELLE]
    
            robotAng += diffa
        
        
            
            for i in range(1,len(linelistmapx)) :
        
                
                linex= linelistmapx[i]
                liney= linelistmapy[i]
                lineLocal = globaltolocal([linex,liney])
                
                anglevx = float(mp.cos(linelistmapa[i]))  *Zoom*60
                anglevy = float(mp.sin(linelistmapa[i]))  *Zoom*60
        
                cv2.line(Globalmap,(lineLocal[0]-int(anglevx),lineLocal[1]-int(anglevy)),(lineLocal[0]+int(anglevx),lineLocal[1]+int(anglevy)),(100,255,100),2)
            
            cv2.imshow('truncated',mask)
                                       
            cv2.imshow('test',warped_img)
        
            #cv2.imshow('tresh',threshold)
        
            #cv2.imshow('tresh2',threshold2)
        
            #cv2.imshow('imgray',blur)
        
            cv2.imshow('denoise',denoise)
        
            cv2.imshow('white',whiteimg)
            cv2.imshow('map',Globalmap)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
