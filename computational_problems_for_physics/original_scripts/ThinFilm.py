""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# ThinFilm.py: Thin film interference by reflection (AJP 72,1248-1253)

from vpython import *
from numpy import *

escene = canvas(width=500, height=500, range=400, background=color.white,\
                 foreground=color.black, title= 'Thin Film Interference')
Rcurve = curve(color=color.red,radius=2)                           # Red intensities 
Gcurve = curve(color=color.green,radius=2)                       # Green intensities
Bcurve = curve(color=color.blue,radius=2)                      # Blue intensities
title  = label(pos=vector(-20,350,0), text='Intensity vs Thickness nA in nm',box=0)
waves  = label(pos=vector(-30,320,0), text='Red, Green, and Blue Intensities',box=0)
trans  = label(pos=vector(-280,300,0),text='Transmission',box=0)
refl   = label(pos=vector(210,300,0),text='Reflection',box=0)
lamR   = 572;   lamB = 430; lamG = 540; i = 0          # R,B, G wavelengths
film = curve(pos=[(-150,-250,0),(150,-250,0),(150,250,0),(-150,250,0),(-150,-250,0)])
Rc = [];  Gc = []; Bc = []                         # R,G,B intensity arrays

nA = arange(0,1250,10)       
delR =  2*pi*nA/lamR+pi; delG = 2*pi*nA/lamG+ pi;  delB =  2*pi*nA/lamB+pi 
intR = (cos(delR/2))**2; intG = (cos(delG/2))**2; intB = (cos(delB/2))**2 
xrp =  300*intR-150; xbp =  300*intB-150;  xgp =  300*intG-150  # Linear TFs  

ap =  -500*nA/1240 +250       
Rc = Rc+[intR];  Gc = Gc+[intG];  Bc = Bc+[intB]                  # Fill I's
Rt = [];  Gt = [];      Bt = []
DelRt =     4*pi*nA/lamR;     DelGt =  4*pi*nA/lamG;   DelBt =  4*pi*nA/lamB
IntRt =     cos(DelRt/2)**2;  IntGt = cos(DelGt/2)**2; IntBt = cos(DelBt/2)**2     
xRpt =      300*intR-150;     xBpt =  300*intB-150;    xGpt =  300*intG-150 
Rt =        Rt + [intR];      Gt = Gt + [intG];        Bt = Bt + [intB]
ap =       -500*nA/1240 +250                                  #  Film height

for nA in range (0,125):    
    col = vector(intR[nA],intG[nA],intB[nA])                      # RGB reflection
    reflesc = -500*nA/125+250                      
    box(pos=vector(205,reflesc,0),width=0.1,height=10,length=50,color=col)
    colt = vector(IntRt[nA],IntGt[nA],IntBt[nA])          # Colors by transmission
    box(pos=vector(-270,reflesc,0),width=0.1,height=10, length=50, color=colt) 
    if (nA%20==0):                                # Labels for vertical axis
        prof = nA*10
        escal = -500*nA/125+250
        #print (escal)
        depth = label(pos=vector(-200,escal,0),text='%4d'%prof,box=0)
for i in range(0,1250,10):
    dlR =  2*pi*i/lamR+pi
    dlG = 2*pi*i/lamG+ pi
    dlB =  2*pi*i/lamB+pi 
    inR = (cos(dlR/2))**2
    inG = (cos(dlG/2))**2
    inB = (cos(dlB/2))**2 
   
    #delB =  2*pi*i/lamB+pi 
    xr =  300*inR-150
    xb =  300*inB-150
    xg =  300*inG-150 
    ar =  -500*i/1240 +250  
    #print('dlR',inR,xr,ar)
    Rcurve.append(pos=vector( xr,ar,0))   
    Bcurve.append(pos=vector( xb,ar,0))   
    Gcurve.append(pos=vector( xg,ar,0))   