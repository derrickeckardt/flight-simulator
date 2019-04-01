#!/usr/bin/env python3
import numpy as np
from math import *
import matplotlib
matplotlib.use('Agg')  # https://stackoverflow.com/questions/37604289/tkinter-tclerror-no-display-name-and-no-display-environment-variable
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
import matplotlib.animation as animation

print("Simulating flight.  Expected run time of one minute or less")

# perform matrix transformation
def matrix_transform(tx,ty,tz,yaw,tilt,twist, focal):
    focal_matrix = np.array([[focal,0,0],[0,focal,0],[0,0,1]]) 
    tilt_matrix = np.array([[1,0,0],[0,cos(tilt),-sin(tilt)],[0,sin(tilt),cos(tilt)]])
    twist_matrix = np.array([[cos(twist),0,-sin(twist)],[0,1,0],[sin(twist),0,cos(twist)]])
    yaw_matrix = np.array([[cos(yaw),-sin(yaw),0],[sin(yaw),cos(yaw),0],[0,0,1]])
    translate_matrix = np.array([[1,0,0,tx],[0,1,0,ty],[0,0,1,tz]])
    final_matrix = np.matmul(focal_matrix,tilt_matrix)
    final_matrix = np.matmul(final_matrix,twist_matrix)
    final_matrix = np.matmul(final_matrix,yaw_matrix)
    final_matrix = np.matmul(final_matrix,translate_matrix)
    return final_matrix

# initialize plane pose (translation and rotation)
(tx, ty, tz) = (0, 0, -10) # (digits)
(yaw, tilt, twist) = (pi, -pi/2, 0)
focal = 0.002

# this function gets called every time a new frame should be generated.
def animate_above(frame_number): 
    global tx, ty, tz, yaw, tilt, twist, focal

    # for oval flight
    # equation of an ellipse
    # y^2 / b^2  + x^2 / a^2  = 1
    # using parametric equations
    a = -500
    b = -600
    tx = a * sin(yaw+(frame_number*pi/180))
    ty = (b*-1) - b * cos(yaw+(frame_number*pi/180))
    # to vary elelvation
    c = -100
    tz = c * sin(frame_number*pi/360)
    yaw_i = pi - (frame_number*pi/180)
    # print(frame_number, tx,ty,tz,yaw_i/pi) - testing code
    
    tmatrix = matrix_transform(tx, ty, tz, yaw_i, tilt, twist, focal)
    # print(tmatrix)

    pr=[]
    pc=[]
    for p in pts3:
        px = (p[0])
        py = (p[1]+ty)
    
        p_a = np.array([px,py,p[2],1])
        p_b = np.matmul(tmatrix,p_a)
        # print(p, p_b)

        if p_b[2] <= 0:
            pr += [-focal * p_b[0] / p_b[2]]
            pc += [-focal * p_b[1] / p_b[2]] 

    plt.cla()
    plt.gca().set_xlim([-.000002,.000002]) #[min(pr),max(pr)]
    plt.gca().set_ylim([-0.000001,0.000001])  #[min(pc),max(pc)]

    # take-off flight only, commented out for oval flight instead.
    # ty+=2
    # tz+= -2

    line, = plt.plot(pr, pc, 'k',  linestyle="", marker=".", markersize=2)

    return line,

# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [ [ float(x) for x in l.split(" ") ] for l in f.readlines() ]
    
# create animation!
fig, ax  = plt.subplots()
frame_count = 360
ani = animation.FuncAnimation(fig, animate_above, frames=range(0,frame_count))

# uncomment if you want to save your animation as a movie. :)
file_name = "movie_oval.mp4"
ani.save(file_name, fps=24)

print("Flight path outputted to '"+file_name+"'.  It's a dizzying ride.")