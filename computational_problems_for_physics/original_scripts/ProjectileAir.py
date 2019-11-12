""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# ProjectileAir.py: Order dt^2 projectile trajectory + drag

from vpython import *
#from visual.graph import *
from numpy import *

v0 = 22.;   angle = 34.;   g = 9.8;   kf = 0.8;   N = 5
v0x = v0*cos(angle*pi/180.);   v0y = v0*sin(angle*pi/180.)
T = 2.*v0y/g;   H = v0y*v0y/2./g;   R = 2.*v0x*v0y/g
print('No Drag T =', T,', H =', H,', R =', R)

graph1 = graph(title='Projectile with & without Drag',xtitle='x',ytitle='y',xmax=R,xmin=-R/20.,ymax=8,ymin=-6.0)
funct = gcurve(color=color.red)
funct1 = gcurve(color=color.green)

def plotNumeric(k):
 vx = v0*cos(angle*pi/180.)
 vy = v0*sin(angle*pi/180.)
 x = 0.0
 y = 0.0
 dt =  vy/g/N/2.
 print("\n       With Friction  ")
 print("       x            y")
 for t in arange(0,0.7*T,0.1):
    #rate(30)
    dt=0.1
    vx = vx - k*vx*dt
    vy = vy - g*dt - k*vy*dt
    x = x + vx*dt
    y = y + vy*dt
    funct.plot(pos=(x,y))
    print(" %13.10f  %13.10f "%(x,y))
		
def plotAnalytic():
    v0x = v0*cos(angle*pi/180.)
    v0y = v0*sin(angle*pi/180.)
    dt = 2.*v0y/g/N
    print("\n       No Friction  ")
    print("        x            y")
    for t in arange(0,N,0.1):
        #rate(30)
        #t = i*dt
        x = v0x*t
        y = v0y*t -g*t*t/2.
        funct1.plot(pos=(x,y))
        print(" %13.10f  %13.10f"%(x ,y))
        
plotNumeric(kf)
plotAnalytic() 
