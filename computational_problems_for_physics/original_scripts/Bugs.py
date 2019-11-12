""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
	 
# Bugs.py The Logistic map

from vpython import *

m_min = 1.0;      m_max = 4.0;       step = 0.01
graph1 = graph(width=300, height=300, title='Logistic Map',
   xtitle='m', ytitle='x', xmax=4., xmin=1., ymax=1., ymin=0.,
   background=color.black)
gcur=gcurve(color=color.red)
pts = gdots( color = color.green,size=0.00001)
lasty = int(1000 * 0.5)         # Eliminates some points
count = 0                       # Plot every 2 iterations
for m in arange(m_min, m_max, step):
    y = 0.5
    for i in range(1,201,1):    y = m*y*(1-y)   # Avoid transients
    for i in range(201,402,1):  y = m*y*( 1 - y) 
    for i in range(201, 402, 1):    # Avoid transients
        oldy=int(1000*y)
        y = m*y*(1 - y)   
        inty = int(1000 * y)
        if  inty != lasty and count%2 == 0: pts.plot(pos=(m,y))  # Avoid repeats
        lasty = inty
        count   += 1
