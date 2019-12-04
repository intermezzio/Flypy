import matplotlib.pyplot as plt
import pandas as pd

drone_props = pd.read_csv("drone_props_roll1.csv")

drone_props.plot()

plt.show()
