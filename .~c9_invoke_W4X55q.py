#!/usr/bin/env python3
import numpy as np
from math import *
import matplotlib
matplotlib.use('Agg')  # https://stackoverflow.com/questions/37604289/tkinter-tclerror-no-display-name-and-no-display-environment-variable
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
import matplotlib.animation as animation

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
(tx, ty, tz) = (0, 0, 0) # (digits)
(yaw, tilt, twist) = (0, -pi/2, 0)
focal = 0.002

# this function gets called every time a new frame should be generated.
def animate_above(frame_number): 
    global tx, ty, tz, yaw, tilt, twist, focal

    tmatrix = matrix_transform(tx, ty, tz, yaw, tilt, twist, focal)
    # print(tmatrix)

    pr=[]
    pc=[]
    for p in pts3:
        px = (p[0])
        py = (p[1]+ty)
    
        p_a = np.array([px,py,p[2],1])
        p_b = np.matmul(tmatrix,p_a)
        # print(p, p_b)

        if p_b[2] >= 0:
            pr += [-focal * p_b[0] / p_b[2]]
            pc += [-focal * p_b[1] / p_b[2]] 
        # print(p_b[0] / p_b[2], p_b[1] / p_b[2], p_b[2])
    # print(max(pr), min(pr),max(pc), min(pc))

    plt.cla()
    plt.gca().set_xlim([-.000002,.000002]) #[min(pr),max(pr)]
    plt.gca().set_ylim([-0.000001,0.000001])  #[min(pc),max(pc)]

    ty+=20
    tz+=0

    line, = plt.plot(pr, pc, 'k',  linestyle="", marker=".", markersize=2)

    return line,

# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [ [ float(x) for x in l.split(" ") ] for l in f.readlines() ]
    
# create animation!
fig, ax  = plt.subplots()
frame_count = 35
ani = animation.FuncAnimation(fig, animate_above, frames=range(0,frame_count))

# uncomment if you want to save your animation as a movie. :)
ani.save("movie.mp4")

plt.show()