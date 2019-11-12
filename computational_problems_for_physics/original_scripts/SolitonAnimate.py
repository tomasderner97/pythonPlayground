""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
#sol.radius = 1.0                      # thickness of line
ds = 0.4                              # Delta x
dt = 0.1                              # Delta t
#max = 2000                            # Numb t steps
mu = 0.1;                             # Mu from KdeV equation
eps = 0.2;                            # Epsilon from KdeV eq
mx = 101                              # grid in x max
fac = mu*dt/(ds**3)                   # combo

# Initialization
u = np.zeros( (mx, 3), float)        # Soliton amplitude 
def init():
   for  i in range(0, mx):            # Initial wave
      u[i, 0] = 0.5*(1.-( (math.exp(2*(0.2*ds*i-5.))-1)/(math.exp(2*(0.2*ds*i-5.) )+ 1)))
   u[0, 1] = 1.
   u[0, 2] = 1.
   u[mx-1, 1] = 0.
   u[mx-1, 2] = 0.                 # End points
init()   

k=range(0,mx)   
fig=plt.figure()                   # figure to plot (a changing line)
# select axis; 111: only one plot, x,y, scales given
ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, mx), ylim=(0, 3))
ax.grid()                          # plot a grid
plt.ylabel("Height")               # temperature of each point of the bar
plt.title("Soliton (runs very slowly)")
line, = ax.plot(k, u[k,0],"b", lw=2)    

for  i in range (1, mx - 1 ):             # First time step
    a1 = eps*dt*(u[i + 1, 0] + u[i, 0] + u[i - 1, 0])/(ds*6.)     
    if i>1 and  i < mx-2:
        a2 = u[i + 2, 0]  +  2.*u[i - 1, 0] - 2.*u[i + 1, 0] - u[i - 2, 0]
    else:
      a2 = u[i - 1, 0] - u[i + 1, 0]
    a3 = u[i + 1, 0] - u[i - 1, 0] 
    u[i, 1] = u[i, 0] - a1*a3 - fac*a2/3.

# later time steps

def animate(num):                       # Following next time steps
    for i in range(1, mx - 2):
          a1 = eps*dt*(u[i + 1, 1] + u[i, 1] + u[i - 1, 1])/(3.*ds)
          if i>1 and i < mx - 2:
            a2 = u[i + 2, 1] + 2.*u[i - 1, 1] - 2.*u[i + 1, 1]  - u[i - 2, 1]
          else:
             a2 = u[i - 1, 1] - u[i + 1, 1]  
          a3 = u[i + 1, 1] - u[i - 1, 1] 
          u[i, 2] = u[i, 0] - a1*a3 - 2.*fac*a2/3.
    line.set_data(k,u[k,2])     # data to plot (x,y)=(position,height) 
    #for m in range(0, mx):     # Recycle array
    u[k, 0] = u[k, 1]             
    u[k, 1] = u[k, 2]
    return line,

ani = animation.FuncAnimation(fig, animate,1)
                                # Finish plot
plt.show()
print("finished") 
