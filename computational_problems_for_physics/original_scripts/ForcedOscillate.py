""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
    
# ForcedOsc.py Driven Oscillator with Matplotlib

import numpy as np, matplotlib.pylab as plt
from rk4Algor import rk4Algor

F=1; m=1;  mu=0.001; omegaF=2; k=1  # Constants                              
omega0 = np.sqrt(k/m)                # Natural frequency 
y = np.zeros((2))
tt = []; yPlot=[]                  # Empty list init  

def f(t,y):                      # RHS force function
    freturn = np.zeros((2))            # Set up 2D array       
    freturn[0] = y[1]
    freturn[1] = 0.1*np.cos(omegaF*t)/m-mu*y[1]/m-omega0**2*y[0]
    return freturn
 
y[0] = 0.1     # initial conditions:x
y[1] = 0.3     # init cond speed
f(0,y)         # call function for t=0 with init conds.
dt = 0.01;   i = 0
for t in np.arange(0,100,dt):    
    tt.append(t)
    y = rk4Algor(t,dt,2, y, f)    # call rk4   
    yPlot.append(y[0])         # Change to y[1] for velocity
    i = i+1
plt.figure()
plt.plot(tt,yPlot) 
plt.title('$\omega_f$=2,k=1,m=1,$\omega_0$=1,$\lambda = 0.001$')  
plt.xlabel('t')
plt.ylabel('x')
plt.show()