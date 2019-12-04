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

t_end = 2
dt = 0.001
drone = Drone()
# Hover speed
init_speed = 5.1012
drone.change_rotor_speed([init_speed + 0.1, init_speed - 0.1, init_speed + 0.1, init_speed - 0.1])

drone_props = pd.DataFrame(columns=["x", "y", "z", "vx", "vy", "vz", "roll", "pitch", "yaw"])
drone_props.loc[0] = drone.get_params()
drone_commands = {1: [hover_speed, hover_speed, 0, 0]}

for index, i in enumerate(np.arange(0, t_end, dt)):
    if i in drone_commands.keys():
        drone.change_rotor_speed(drone_commands[i])
    drone.update(dt=dt)
    drone_props.loc[i] = drone.get_params()

print(drone_props)
