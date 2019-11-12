  """ From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
   by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# DLA.py:   Diffusion Limited aggregation 

from vpython import *
import  numpy as np, random
Maxx=500;    Maxy=500                 #canvas width, height
escene = canvas(width=Maxx, height=Maxy,title='Diffusion Limited Aggregation',
                  range=40)
escene.center=vector(0,0,15)                

def gauss_ran():
    r1 = random.random()
    r2 = random.random()
    fac = sqrt(-2*log(r1))
    mem = int(fac*20000*cos(2*pi*r2))
    return mem
    
rad = 40.0                          #radius of yellow circle
step = 0
trav = 0                             # to check if random walk ends
size = 60                            # array size x size                          
max = 500                           # max number of ball generations
grid =np.zeros((size,size))        # Particle positions grid 1 if occupied 
ring(pos=vector(0,0,0),axis=vector(0,0,1),radius=rad,thickness=0.5,color=color.cyan)
grid[30,30] = 1                     # particle in center
sphere(pos=vector(4*30/3-40,-4*30/3+40,0),radius=.8,color=color.green)  
ball=sphere(radius=0.8)             # Moving ball
                    
while True:              # generates new ball and its motion,"infinite loop"
    hit = 0                         # ball doesn't hit a fixed one
    angle = 2. *pi * random.random()  
    x =rad * cos(angle)         
    y =rad * sin(angle)         
    dist = abs(gauss_ran() )        # length of random walk 
    # print(dist)
    # sphere(pos=(x,y),color=color.magenta) # uncomment to see start point
    trav = 0
    ballcolor=(color.yellow)
    while( hit==0 and x<40 and x>-40 and y<40 and y>-40 and trav < abs(dist)):
        if(random.random() <0.5): step=1   #probability advance or retreat
        else: step =- 1;
        xg = int(0.7*x+30)           # transform. coord for indexes
        yg = int(-0.7*y+30+0.5)      # xg=m*x*b, 30=0*m+b, 58=m*40+b
        if ((grid[xg+1,yg]+grid[xg-1,yg]+grid[xg,yg+1]+grid[xg,yg-1]) >= 1):
          hit = 1                       # moving ball hits a fixed ball
          grid[xg,yg] = 1               # this position is occupied now
          sphere(pos=vector(x,y,0),radius=0.8,color=color.yellow)
        else:
            if ( random.random() < 0.5 ):  x+= step  # move right
            else: y+= step                    #prob 1/2 to move up
            xp = 80*x/56.0-40                  
            yp = -80*y/56.+40                          
            ball.pos = vector(xp,yp,0)     # xp=m*x+b, -40=m*2 +b, 40=m*58-40
            rate(10000)                      # to change ball speed
        trav=trav+1     #increments distance, must be smaller than dist 
