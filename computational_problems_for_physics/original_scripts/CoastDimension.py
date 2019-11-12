""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# CoastDimension.py: fractal dimension analysis of coastline

import random, numpy as np
import matplotlib.pyplot as plt, matplotlib.mlab as mlab

MinX = 0;  MaxX = 200;  MinY = 0;  MaxY = 60
coast = np.zeros((200));  nboxes = [];  scales = []       
for i in range(0,5000):         
    spot = int(200*random.random()) 
    if (spot == 0):            # Hitting edge = filling hole
        if (coast[spot] < coast[spot+1]): coast[spot]  =  coast[spot+1]
        else: coast[spot] =  coast[spot] + 1
    else:
        if (spot == 199):                    # Extreme right
            if (coast[spot] < coast[spot-1]): coast[spot] = coast[spot-1]
            else: coast[spot] = coast[spot] + 1
        else:                              # All other cases
            if ((coast[spot]<coast[spot - 1])and
                (coast[spot]<coast[spot + 1])):
                if (coast[spot-1] > coast[spot+1]): coast[spot] = coast[spot-1]
                else: coast[spot] = coast[spot + 1]
            else: coast[spot] = coast[spot] + 1          
i =  range(0,200)
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(12,5) )
axes[0].plot( i,coast) 
p = [0,200]
sc = 1
countbox = 0  
M = 1                                # To plot divisions
for k in range(0,4):                # 4 scales and boxes
  M *= 2          
  cajas = 0
  for j in range (0,M):
    dx = 200/M                          # Horizontal/M
    dy = MaxY/M                               
    q = [MaxY-dy*j,MaxY-dy*j]  # Plot horiz & vert lines
    axes[0].plot(p,q,'r-')
    r = [dx*(j+1),dx*(j+1)]
    ver = [0,60]
    axes[0].plot(r,ver,'r-')               # Vert lines
    plt.pause(0.1)                   # Delay while plot
    for m in range(0,M):
       for i in range(int(m*dx),int((m+1)*dx)):
          if coast[i]<60-dy*j and coast[i]>60-dy*(j+1):
            countbox = 1     # Occupied, count & break
            if countbox ==1:  
                cajas = cajas + 1 
                countbox=0
            break                 # Continue counting 
  nboxes.append(np.log(cajas))               # Log N
  sc = sc*2                         # Multiply scale
  scales.append(np.log(sc))   # Scale = number boxes
  axes[1].plot(scales[k],nboxes[k],'ro')  # Plot logs
axes[0].set_xlabel('x')
axes[0].set_ylabel('Coast')
axes[0].set_title('Box Counting for Fractal Dimension')
m,b=np.polyfit(scales,nboxes,1)        # Linear fit
x= np.arange(0,4,0.1)                   # Plot line
axes[1].plot(x, m*x+ b)
axes[1].set_title('Log(N) vs Log(s)')
axes[1].set_xlabel('log(scale)')
axes[1].set_ylabel('log(N)')
fd="%6.3f"%m            # Convert dimension to string
axes[1].text(1,4,'Fractal dim. ='+ fd,fontsize=15,)
plt.show()
