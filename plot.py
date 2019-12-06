import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
import json
import sys
from math import pi

from drone import Drone
from sweep import moveDrone, cardinalToAngle, angleToCardinal

# Establish the target destination through python cmd line args
target_xyz = (3,3,3) if len(sys.argv) < 4 else tuple(int(i) for i in sys.argv[1:4])
print(target_xyz)

# Open the json dict with all data
# (or calculate it if it doesn't already exist)
try:
	raise FileNotFoundError
	with open(f"data/x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.json",
				'r', encoding='utf-8') as data:
		full_dict = json.loads(data.read())
except FileNotFoundError:
	moveDrone(*target_xyz)
	with open(f"data/x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.json",
				'r', encoding='utf-8') as data:
		full_dict = json.loads(data.read())

# Extract motion data from full_dict
tries = full_dict["tries"]
optimal = full_dict["key"]

# Keep these values constant - consistent with the optimal solution
# (so we only plot 3 dimensions of data)
right_rollpitch_power = optimal["rollpitch_power"]
right_yaw = optimal["yaw_power"]

# Create figure
# Plot adapted from https://matplotlib.org/3.1.1/gallery/mplot3d/surface3d.html
fig = plt.figure()
ax = Axes3D(fig)

# Establish X and Y values and convert to 2D arrays
orig_X = [int(i) for i in tries.keys()]
cardinal_angles = tries["580"].keys()
orig_Y = np.arange(0,2*pi, pi/4)
X, Y = np.meshgrid(orig_X, orig_Y) # 1D => 2D

# Create Z array
Z = list()
for i in range(len(X)):
	Z.append(list())
	for j in range(len(X[0])):
		new_z = tries[str(X[i][j])][angleToCardinal(Y[i][j])][str(right_rollpitch_power)][str(right_yaw)]["dist"]
		Z[-1].append(new_z)
Z = np.array(Z)

for i, row in enumerate(Y):
	for j, item in enumerate(row):
		Y[i][j] = int(item * 180 / pi)
# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm_r,
                       linewidth=0, antialiased=False)

# Customize the z axis
ax.set_zlim(0)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.suptitle(f"Drone Trajectory to ({target_xyz[0]},{target_xyz[1]},{target_xyz[2]})")
ax.set_xlabel("Average Rotor Speed (Hz)")
ax.set_ylabel("Roll-Pitch Bearing (deg)")
ax.zaxis.set_rotate_label(True)
ax.set_zlabel("Distance to target (m)", rotation = 0)

# Add a color bar which maps values to colors
fig.colorbar(surf, shrink=0.5, aspect=5)

print(optimal["r_speed"])

# Save a png file
plt.savefig(f"data/x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.png")

# Animation adapted from
# https://pythonmatplotlibtips.blogspot.com/2018/01/rotate-azimuth-angle-animation-3d-python-matplotlib-pyplot.html
def animate(i):
    # Azimuth angle : 0 deg to 360 deg
    ax.view_init(elev=10, azim=i*.5)
    return fig,

# Animate
ani = animation.FuncAnimation(fig, animate, init_func=lambda: (fig,),
                               frames=720, interval=20, blit=True)
# save gif
ani.save(f"data/x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.gif",
							   writer='imagemagick',fps=1000/50)
