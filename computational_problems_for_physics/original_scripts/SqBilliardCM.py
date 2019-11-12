""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# SqBillardCM.py: Animated classical billiards on square table

from vpython import *

dt = 0.01;   Xo = -90.;  Yo =  -5.4; 
v = vector(13.,13.1,0)
r0 = r= vector(Xo,Yo,0); eps = 0.1;  Tmax = 500; tp = 0
scene = canvas(width=500, height=500, range=120,\
                background=color.white, foreground=color.black)
table = curve(pos=([(-100,-100,0),(100,-100,0),(100,100,0),
	(-100,100,0),(-100,-100,0)]))
ball = sphere(pos=vector(Xo,Yo,0),color=color.red, radius=0.1,make_trail=True)

for t in arange(0,Tmax,dt):
    rate(5000) 
    tp = tp + dt   
    r = r0 + v*tp
    if(r.x>= 100 or r.x<=-100):         # Right and left walls
       v = vector(-v.x,v.y,0)
       r0 = vector(r.x,r.y,0)
       tp = 0
    if(r.y>= 100 or r.y<=-100):         # Top and bottom walls
       v = vector(v.x,-v.y,0)
       r0 = vector(r.x,r.y,0)
       tp = 0
    ball.pos=r           
