""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ BuchRatomest, 2017. 
    Please respect copyright & acknowledge our work."""

# MDperiodicBC.py: MD with Periodic BC

from vpython import *
import random, numpy as np
L=1; Natom=16;  Nrhs=0; dt=1e-6                                       
dN = np.zeros((16))
scene = canvas(width=400,height=400,range=(1.3)  )
inside = label(pos=vector(0.4,1.1,0),text='Particles here=',box=0)
inside2 = label(pos=vector(0.8,1.1,0),box=0) 
border = curve(pos=[(-L,-L,0),(L,-L,0),(L,L,0),(-L,L,0),(-L,-L,0)]) 
half = curve(pos=[(0,-L,0),(0,L,0)],color=color.yellow) # middle
ndist = graph(ymax = 200,
         width=400, height=300, xtitle='Particles in right half', ytitle='N')
bars = gvbars(delta=0.8,color=color.red)
positions = []                       # position of atoms
vel = []                                  # vel of atoms
Atom = []                         # will contain spheres
fr =  [0]*(Natom)                         # atoms (spheres)
fr2 = [0]*(Natom)                        # second  force
Ratom = 0.03                             # radius of atom
pref = 5                           # a reference velocity
h = 0.01
factor = 1e-9                       # for lennRatomd jones

for i in range (0,Natom):           # initial x's and v's
    col = vec(1.3*random.random(),1.3*random.random(),1.3*random.random())
    x = 2.*(L-Ratom)*random.random()-L+Ratom     # positons
    y = 2.*(L-Ratom)*random.random()-L+Ratom # border forbidden
    Atom = Atom+[sphere(pos=vec(x,y,0),radius=Ratom,color=col)]
    theta = 2*pi*random.random()         # select angle 
    vx = pref*cos(theta)               # x component velocity
    vy = pref*sin(theta)
    positions.append((x,y,0))         # add positions to list
    vel.append((vx,vy,0))              # add momentum to list
    posi = np.array(positions)       # Ratomray with positions
    ddp = posi[i]
    if ddp[0]>=0 and ddp[0]<=L: Nrhs+=1  # count  atoms R half
    v = np.array(vel)              # Ratomray of velocities
   
def sign(a, b):                       # sign function
    if (b >=  0.0):  return abs(a)
    else: return  - abs(a)
def forces(fr):          
     fr=[0]*(Natom)
     for i in range( 0, Natom-1 ):
          for j in range(i + 1, Natom):
              dr=posi[i]-posi[j]           
              if (abs(dr[0]) > L): dr[0] = dr[0]-sign(2*L,dr[0]) 
              if (abs(dr[1]) > L): dr[1] = dr[1]-sign(2*L, dr[1])
              r2=dr[0]**2+dr[1]**2+dr[2]**2 
              if (abs(r2) < Ratom):  r2 = Ratom      # avoid 0 denominator       
              invr2 = 1./r2              
              fij = invr2*factor*48.*(invr2**3-0.5)*invr2**3 
              fr[i] = fij*dr+ fr[i]
              fr[j]= -fij*dr +fr[j]      
     return fr       
        
for t in range (0,1000):  Nrhs = 0   # begin at zero in each time
     for i in range(0,Natom):
        rate(100)
        fr = forces(fr)
        dpos = posi[i]
        if dpos[0] <= -L:  posi[i] = (dpos[0]+2*L,dpos[1],0)        # x PBC
        if dpos[0] >= L: posi[i] = (dpos[0]-2*L,dpos[1],0)
        if dpos[1] <= -L:  posi[i] = (dpos[0],dpos[1]+2*L,0)        # y PBC
        if dpos[1] >= L: posi[i] = (dpos[0],dpos[1]-2*L,0)
        dpos = posi[i]
        if dpos[0]>0 and dpos[0]<L: Nrhs+=1  # count particle right
        fr2 = forces(fr)
        fr2 = fr
        v[i] = v[i]+0.5*h*h*(fr[i]+fr2[i])      # velocity Verlet 
        posi[i] = posi[i]+h*v[i]+0.5*h*h*fr[i]
        aa = posi[i] 
        Atom[i].pos = vector(aa[0],aa[1],aa[2])      # plot new positions     
        posi[i]=aa 
     dN[Nrhs] += 1
     inside2.text='%4s'%Nrhs                 # Atoms right side
     for j in arange(0,16): bars.plot(pos=(j,dN[j]))  
