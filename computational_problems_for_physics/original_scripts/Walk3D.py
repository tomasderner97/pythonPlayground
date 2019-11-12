""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# Walk3D.py  3-D Random walk with 3-D graph
 
from vpython import *
import random

random.seed(None)                  # None => system clock
jmax = 1000
xx =yy = zz =0.0                           # Start at origin

graph1 = canvas(x=0,y=0,width = 500, height = 500, 
	title = '3D Random Walk', forward=vector(-0.6,-0.5,-1))
pts   = curve(x=list(range(0, 100)), radius=10.0,
	color=color.yellow)    
xax   = curve(x=list(range(0,1500)), color=color.red, 
	pos=[vector(0,0,0),vector(1500,0,0)], radius=10.)
yax   = curve(x=list(range(0,1500)), color=color.red, 
	pos=[vector(0,0,0),vector(0,1500,0)], radius=10.)
zax   = curve(x=list(range(0,1500)), color=color.red, 
	pos=[vector(0,0,0),vector(0,0,1500)], radius=10.)
xname = label( text = "X", pos = vector(1000, 150,0), box=0)
yname = label( text = "Y", pos = vector(-100,1000,0), box=0)
zname = label( text = "Z", pos = vector(100, 0,1000), box=0)
 
for i in range(1, 100):
    xx += (random.random() - 0.5)*2.  # -1 =< x =< 1  
    yy += (random.random() - 0.5)*2.  # -1 =< y =< 1
    zz += (random.random() - 0.5)*2.  # -1 =< z =< 1
    pts.append(pos=vector ( 200*xx - 100, 200*yy - 100, 200*zz - 100))
    rate(100)
print("Walk's distance R =", sqrt(xx*xx + yy*yy+zz*zz))

