import numpy as np
from math import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# this function gets called every time a new frame should be generated.
# 
def animate_above(frame_number): 
    global tx, ty, tz, compass, tilt, twist

    ty+=20

    pr=[]
    pc=[]
    for p in pts3:
        pr += [p[0]/100000]
        pc += [(p[1]+ty)/100000]

    plt.cla()
    plt.gca().set_xlim([-0.002,0.002])
    plt.gca().set_ylim([-0.002,0.002])
    line, = plt.plot(pr, pc, 'k',  linestyle="", marker=".", markersize=2)
    return line,

# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [ [ float(x) for x in l.split(" ") ] for l in f.readlines() ]

# initialize plane pose (translation and rotation)
(tx, ty, tz) = (0, 0, -10)
(compass, tilt, twist) = (0, pi/2, 0)

# create animation!
fig, ax  = plt.subplots()
frame_count = 50
ani = animation.FuncAnimation(fig, animate_above, frames=range(0,frame_count))

# uncomment if you want to save your animation as a movie. :)
#ani.save("movie.mp4")

plt.show()


