""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
		
# QMC.py: Quantum MonteCarlo, Feynman path integration from initial st line
 
import random
from vpython import *
import numpy as np

N = 101;            M = 101;           xscale = 10. # Initialize  
path = np.zeros((M), float); prob =np.zeros([M], float)            
trajec = canvas(width = 300, height = 500, title = 'Spacetime Trajectories')
trplot = curve( color = color.magenta, display = trajec, radius=0.8)

def trjaxs():                 # plot axis for trajectories
   trax = curve(pos = [( - 97,  - 100,0), (100,  - 100,0)], color = color.cyan, canvas = trajec) 
   curve(pos = [(0,  - 100,0), (0, 100,0)], color = color.cyan, canvas = trajec)  
   label(pos =vector (0,  - 110,0), text = '0', box = 0, canvas = trajec)
   label(pos =vector (60,  - 110,0), text = 'x', box = 0, canvas = trajec) 

wvgraph = canvas(x = 340, y = 150, width = 500, height = 300, title = 'Ground State Probability')
wvplot = curve(x = range(0, 100), canvas = wvgraph)      # for probability
wvfax = curve(color = color.cyan)

def wvfaxs():                                      # axis for probability
   wvfax = curve(pos = [(-600,-155,0), (800,-155,0)], canvas=wvgraph, color=color.cyan)
   curve(pos = [(0,-150,0), (0,400,0)], display=wvgraph, color=color.cyan)       
   label(pos = vector(-80,450,0), text='Probability', box = 0, canvas = wvgraph)
   label(pos = vector(600,-220,0), text='x', box=0, canvas=wvgraph)
   label(pos = vector(0,-220,0), text='0', box=0, canvas=wvgraph)   
   
trjaxs()
wvfaxs()                                              # plot axes 

def energy(path):                                        # HO energy
    sums = 0.                                
    for i in range(0, N-2):  sums += (path[i+1] - path[i])*(path[i+1] - path[i]) 
    sums += path[i+1]*path[i+1]; 
    return sums 

def plotpath(path):                            # plot trajectory in xy scale
   for j in range (0, N):                     
       trplot.append(pos=vector(20*path[j], 2*j - 100,0))
       
def plotwvf(prob):                                 # plot prob
    for i in range (0, 100):
       wvplot.color = color.yellow
       wvplot.append(pos=vector(  8*i - 400 , 4.0*prob[i] - 150,0))  
                   
oldE = energy(path)                              # find E of path

#while True:                                     # pick random element
for i in range (0,1500):
    rate(50)                                      # slows paintings
    element = int(N*random() )                    # Metropolis algorithm
    change = 2.0*(random() - 0.5)    
    path[element]   += change                     # Change path
    newE = energy(path);                          # Find new E
    if  newE > oldE and np.exp( - newE + oldE)<= random():
          path[element]   -= change               # Reject
          trplot.clear()      # Erase previous trajctory
          plotpath(path)
          trplot.visible=True   # Make visible new trajectory 
    elem = int(path[element]*16 + 50)        #       if path = 0, elem = 50
    if elem < 0: 
        elem = 0                           # negative case not allowed
    if elem > 100:  
        elem = 100                         # if exceed max
    prob[elem] += 1               # increase probability for that x value
    plotwvf(prob)                         # plot prob
    oldE = newE                
