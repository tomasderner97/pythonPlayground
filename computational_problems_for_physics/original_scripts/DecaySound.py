""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# DecaySound.py spontaneous decay simulation

from vpython import *    # Was: from visual.graph import *
import random, winsound

lambda1 = 0.005                               # Decay constant                      
max = 80.;  time_max = 500;   seed = 68111                                    
number = nloop = max                           # Initial value
graph1 = graph(title ='Spontaneous Decay',xtitle='Time',
                  ytitle = 'Number',xmin=0,xmax=500,ymin=0,ymax=90)
decayfunc = gcurve(color = color.green)

for time in arange(0, time_max + 1):              # Time loop
    for atom in arange(1, number + 1 ):          # Decay loop
        decay = random.random()   
        if (decay  <  lambda1):
            nloop = nloop  -  1                     # A decay
            winsound.Beep(600, 100)              # Sound beep
    number = nloop
    decayfunc.plot( pos = (time, number) )
    rate(30)
