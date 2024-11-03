import matplotlib.pyplot as plt
import numpy as np

#define plots
fig, ax = plt.subplots()

#define coordinates and directions
x,y = np.meshgrid(np.arange(-2, 2, .1), np.arange(-2, 2, .1))
z = x*np.exp(-x**2 - y**2)
v, u = np.gradient(z, .1, .1)

#create quiver plot
ax.quiver(x, y, u, v)

#display quiver plot
plt.show()