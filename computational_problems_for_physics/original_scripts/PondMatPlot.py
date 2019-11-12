""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""
    
#  PondMatPlot.py: Monte-Carlo integration via vonNeumann rejection

import numpy as np, matplotlib.pyplot as plt
 
N,Npts = 100,   5000; 
analyt = np.pi**2                                     
x1 = np.arange(0, 2*np.pi+2*np.pi/N,2*np.pi/N)   
xi = [];  yi = [];  xo = [];  yo = []   
fig,ax = plt.subplots()
y1 = x1 * np.sin(x1)**2                           # Integrand
ax.plot(x1, y1, 'c', linewidth=4)      
ax.set_xlim ((0, 2*np.pi))              
ax.set_ylim((0, 5))                    
ax.set_xticks([0, np.pi, 2*np.pi])     
ax.set_xticklabels(['0', '$\pi$','2$\pi$'])  
ax.set_ylabel('$f(x) = x\,\sin^2 x$', fontsize=20) 
ax.set_xlabel('x',fontsize=20)
fig.patch.set_visible(False)
    
def fx(x):   return x*np.sin(x)**2                  # Integrand
             
j = 0                                    # Inside curve counter
xx = 2.* np.pi * np.random.rand(Npts)          # 0 =< x <= 2pi
yy = 5*np.random.rand(Npts)                      # 0 =< y <= 5
boxarea = 2. * np.pi *5.                         # Box area 
for i in range(1,Npts):  
    #plt.pause(0.000001)          
    if (yy[i] <= fx(xx[i])):                     # Below curve
        xi.append(xx[i])               
        yi.append(yy[i])
        j +=1                           
    else:                           
        yo.append(yy[i])               
        xo.append(xx[i])
   
    area = boxarea*j/(Npts-1)                # Area under curve
ax.plot(xo,yo,'bo',markersize=1)    
ax.plot(xi,yi,'ro',markersize=1)    
ax.set_title('Answers: Analytic = %5.3f, MC = %5.3f'%(analyt,area))
plt.show()