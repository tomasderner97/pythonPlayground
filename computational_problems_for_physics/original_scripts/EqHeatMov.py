""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
   
# EqHeat.py Animated heat equation soltn via fine differences

from numpy import *
import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
 
Nx = 101;   Dx = 0.01414;   Dt = 0.6                                                                 
KAPPA = 210.;  SPH = 900.; RHO = 2700.   # Conductivity, Specific heat,Density                                        
cons = KAPPA/(SPH*RHO)*Dt/(Dx*Dx)        # For algorthim
T = np.zeros( (Nx, 2), float)            # Temp @ first 2 times

def init():
   for ix in range (1, Nx - 1):   T[ix, 0] = 100.0;        # Initial T
   T[0, 0] = 0.0;  T[0, 1] = 0.                 # Ends of bar at T = 0    
   T[Nx - 1, 0] = 0.;  T[Nx - 1, 1] = 0.0
   
init()
k = range(0,Nx)
fig = plt.figure()        
# select axis; 111: only one plot, x,y, scales given
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 105), ylim=(-5, 110.0))
ax.grid()                                               # plot a grid
plt.ylabel("Temperature")      # temperature of each point of the bar
plt.title("Cooling of a bar")
line, = ax.plot(k, T[k,0],"r", lw=2)     # x axis, y values, linewidth=2
plt.plot([1,99],[0,0],"r",lw=10)         # the bar
plt.text(45,5,'bar',fontsize=20)         # text: bar
 
def animate(dum):                        # dummy num, for animation
   for ix in range (1, Nx-1):    
      T[ix, 1] = T[ix, 0] + cons*(T[ix+1,0] + T[ix-1,0] - 2.*T[ix, 0])
   line.set_data(k,T[k,1] )    # data to plot (x,y)=(k,temperature) 
   for ix in range (1, Nx - 1): T[ix, 0] = T[ix, 1]      # Row of 100 positions  
   return line,            
ani = animation.FuncAnimation(fig, animate,1)   # dummy argument: 1
plt.show()
