import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle,Circle
import mpl_toolkits.mplot3d.art3d as art3d

def data_for_cylinder_along_z(center_x,center_y,center_z,radius,height_z):
    
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x + radius
    y_grid = radius*np.sin(theta_grid) + center_y + radius
    z_grid = z_grid + center_z
    return x_grid,y_grid,z_grid



fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
ax = plt.axes(projection='3d')

# pos
x,y,z = 0,0,50
# 長寬高
dx,dy,dz = 10,10,10

p = Circle((x+dx/2,y+dx/2,z),radius=dx/2,color='b')
p2 = Circle((x+dx/2,y+dx/2,z),radius=dx/2,color='b')
ax.add_patch(p)
ax.add_patch(p2)
art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
art3d.pathpatch_2d_to_3d(p2, z=z+dz, zdir="z")

Xc,Yc,Zc = data_for_cylinder_along_z(x,y,z,radius=dx/2,height_z=dz)
ax.plot_surface(Xc, Yc, Zc,alpha=1,color='b')

plt.show()