""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
    
# rk4Duffing.py solve ODE for Duffing Osc via rk4 & Matplotlib

import numpy as np, matplotlib.pylab as plt  
from rk4Algor import rk4Algor

tt =[];  yy = []; vy = []
y = np.zeros((2),float)
a = 0.5;  b = -0.5;  g = 0.02; 
A, w, h = 0.0008, 1., 0.01                                                           
y[0] = 0.09; y[1] =  0.         # Initial x, velocity

def f(t,y):     
    rhs = np.zeros((2))
    rhs[0] = y[1]
    rhs[1] = -2*g*y[1] - a*y[0] - b*y[0]**3 + A*np.cos(w*t)
    return rhs
f(0,y)

for t in np.arange(0,40,h):                      # Time Loop     
    y = rk4Algor(t,h,2,y,f)                        # Call rk4  
    tt.append( t)
    yy.append(y[0])                                    # x(t)
    vy.append(y[1])                                    # v(t)
  
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(12,5) )   
axes[0].plot(tt[1000:],yy[1000:])    # 1000 avoids transients
axes[0].grid()                                          # x(t)
axes[0].set_title('Duffing Oscillator x(t)')         
axes[0].set_xlabel('t')
axes[0].set_ylabel('x(t)')
axes[1].plot(yy[1000:],vy[1000:])            
axes[1].grid()
axes[1].set_title('Phase Space Orbits, Duffing Oscillator')  
axes[1].set_xlabel('x(t)')
axes[1].set_ylabel('v(t)')   
plt.show()
