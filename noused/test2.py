

def getCynByAxis(radius = 1, heightStart = 0, heightEnd = 5, \
    offset = [0, 0, 0], devision = 20, mainAxis = 'z'):
    '''NyanNyanNyan'''
    import numpy as np

    mainAxis = mainAxis.lower()

    theta = np.linspace(0, 2*np.pi, devision)
    cx = np.array([radius * np.cos(theta)]) 
    cz = np.array([heightStart, heightEnd])
    cx, cz = np.meshgrid(cx, cz)
    cy = np.array([radius * np.sin(theta)] * 2)

    if mainAxis == 'z':
        return offset[0] + cx, offset[1] + cy, offset[2] + cz
    elif mainAxis == 'y':
        return offset[0] + cx, offset[1] + cz, offset[2] + cy
    elif mainAxis == 'x':
        return offset[0] + cz, offset[1] + cy, offset[2] + cx
    else:
        raise ValueError("'x', 'y' or 'z' PLZ")

def drawCylinder():
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np

    cx, cy, cz = getCynByAxis(offset = [1, 2, 3], devision = 40,\
        mainAxis = 'z', heightEnd = 100, heightStart = 0,\
        radius = 0.5)

    fig = plt.figure(figsize = (11, 10))
    ax = plt.axes(projection = '3d')
    ax.plot_surface(cx, cy, cz, rstride = 1, cstride = 1,\
        linewidth = 0, alpha = 0.25)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(0, 10)
    plt.show()

if __name__ == '__main__':
    drawCylinder()