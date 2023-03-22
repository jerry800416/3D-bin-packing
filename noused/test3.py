from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.patches import Rectangle,Circle
import mpl_toolkits.mplot3d.art3d as art3d

fig = plt.figure() 
# ax = fig.add_subplot(111, projection='3d') 
ax = plt.axes(projection='3d')

x,y,z = 10,0,0
dx,dy,dz = 12,12,10


p = Circle((x,y),radius=dx/2,color='b')
p2 = Circle((x,y),radius=dx/2,color='b')
ax.add_patch(p)
ax.add_patch(p2)
art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
art3d.pathpatch_2d_to_3d(p2, z=z+dz, zdir="z")

us = np.linspace(0, 2 * np.pi, 32) 
zs = np.linspace(0, 10, 2) 

us, zs = np.meshgrid(us, zs) 

xs = 6 * np.cos(us) 
ys = 6 * np.sin(us) 
ax.plot_surface(xs, ys, zs, color='g') 

plt.show() 