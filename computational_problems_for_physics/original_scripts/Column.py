""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
    
# Column.py: Correlated ballistic deposition

from vpython import *
import random, numpy as np

graph1 = canvas(width = 500, height = 500,         
        title = 'Correlated Ballistic Deposition', range = 250.0)
pts = points(color=color.green, radius=1)
hit = np.zeros( (200))
maxi = 80000;  npoints = 200;  dist = 0;  oldx = 100; oldy = 0          

for i in range(1, maxi):
    r = int(npoints*random.random() )
    x = r - oldx
    y = hit[r] - oldy
    dist = x*x  +  y*y
    prob = 9.0/dist
    pp = random.random()
    if (pp < prob):
        if(r>0 and r<(npoints - 1) ):
            if( (hit[r] >=  hit[r - 1]) and (hit[r] >=  hit[r + 1]) ):
                hit[r] = hit[r] + 1
            else:
                if (hit[r - 1] > hit[r + 1]): hit[r] = hit[r - 1]
                else: hit[r] = hit[r + 1]
        oldx = r
        oldy = hit[r]
        olxc = oldx*2 - 200 # linear transform 0<oldx<200  - >  - 200<olxc<200
        olyc = oldy*4 - 200 
        pts.append(pos=vector(olxc,olyc,0)) 
