import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
import json
import sys
from math import pi

from drone import Drone
from sweep import moveDrone, cardinalToAngle, angleToCardinal

target_xyz = (3,3,3) if len(sys.argv) < 4 else [int(i) for i in sys.argv[1:4]]

try:
	with open(f"x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.json",'r', encoding='utf-8') as data:
		full_dict = json.loads(data.read())
	# full_dict = json.loads(open(f"x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.json",'r'))
except:
	moveDrone(*target_xyz)
	with open(f"x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.json",'r', encoding='utf-8') as data:
		full_dict = json.loads(data.read())

tries = full_dict["tries"]
optimal = full_dict["key"]

right_rollpitch_power = optimal["rollpitch_power"]
right_yaw = optimal["yaw_power"]

fig = plt.figure()
ax = Axes3D(fig)#.gca(projection='3d')

# Make data.
orig_X = [int(i) for i in tries.keys()]
cardinal_angles = tries["580"].keys()
orig_Y = np.arange(0,2*pi, pi/4)
X, Y = np.meshgrid(orig_X, orig_Y)
R = np.sqrt(X**2 + Y**2)
Z = list()
for i in range(len(X)):
	Z.append(list())
	for j in range(len(X[0])):
		new_z = tries[str(X[i][j])][angleToCardinal(Y[i][j])][str(right_rollpitch_power)][str(right_yaw)]["dist"]
		Z[-1].append(new_z)
Z = np.array(Z)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(0, 15)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.savefig(f"x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.png")
plt.show()