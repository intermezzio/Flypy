import numpy as np
import scipy as scp
import sympy as smp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
    "yaw",
]

# data = pd.DataFrame(cols=params)

t_end = 100
dt = 1
drone = Drone(rotor_radius=15,
              weight=50,
              size=10,
              m_of_i=1)

for i in range(0, t_end, dt):
    drone.update(dt=dt)
    ret = drone.get_params()
