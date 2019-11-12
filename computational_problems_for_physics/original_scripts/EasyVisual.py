""" From "COMPUTATIONAL PHYSICS" & "COMPUTER PROBLEMS in PHYSICS"
    by RH Landau, MJ Paez, and CC Bordeianu (deceased)
    Copyright R Landau, Oregon State Unv, MJ Paez, Univ Antioquia, 
    C Bordeianu, Univ Bucharest, 2018. 
    Please respect copyright & acknowledge our work."""

# EasyVisual.py :   Simple graph object using Vpython

from vpython import *                   # Import Vpython

graph1=graph(align='left',width=400, height=400,background=color.white
             ,foreground=color.black) #align to left of widow
Plot1=gcurve(color=color.red)              # gcurve method 
for x in arange(0,8.1,0.1):                  # x range
    Plot1.plot(pos=(x,5*cos(2*x)*exp(-0.4*x)))
graph2=graph(align='right',width=400, height=400,background=color.white,
                foreground=color.black, title='2-D Plot',
                xtitle='x',ytitle='f(x)') # align to right of window
Plot2=gdots(color=color.black)               # Dots
for x in arange(-5,5,0.1):
    Plot2.plot(pos=(x,cos(x)))               # plot dots
  
