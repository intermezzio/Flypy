import numpy as np
import pandas as pd
# import scipy as scp
# import sympy as smp
# import matplotlib.pyplot as plt
# import seaborn as sns

from drone import Drone


params = [
    "x",
    "y",
    "z",
    "v_x",
    "v_y",
    "v_z",
    "roll",
    "pitch",
    "yaw"
]

# data = pd.DataFrame(cols=params)

t_end = 100
dt = .1
drone = Drone()

drone_props = pd.DataFrame(columns=["x", "y", "z", "vx", "vy", "vz", "roll", "pitch", "yaw"])
drone_props.loc[0] = drone.get_params()

for index, i in enumerate(np.arange(0, t_end, dt)):
    drone.update(dt=dt)
    drone_props.loc[i] = drone.get_params()

print(drone_props)
