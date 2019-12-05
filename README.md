# Flypy

This code models the flight of a quadrotor by supplying rotor speeds. Given a target location, the code will find out what rotor speeds help the drone arrive at the desired location.

## Using the software

Clone this repository and run the plot.py script to model your drone. In the terminal, run it as so:

```
python plot.py 1 2 3
```
(1,2,3) represents a point in 3D cartesian coordinate space where the drone is to arrive. Replace these values with a point of your own to alter the trajectory.

## How it Works

### drone.py
This code simulates the flight of a drone by inputting the rotor speeds and using kinematic equations to determine the resulting flight of the drone.

### sweep.py
The drone is tested with different values for roll, pitch, yaw, and thrust, and trajectories are compared to find the most accurate one. This outputs a json file with all trajectory tests and a determined optimal trajectory.

### plot.py
To present the data, a heatmap is generated with average rotor speed on the x-axis and roll/pitch angle on the y-axis. The z-axis states how close the trajectory is to the desired location. This data is presented in a 3D graph and saved as a png and gif (pronounced [jif](https://www.cnn.com/2013/05/22/tech/web/pronounce-gif/index.html)). The png is for static viewing and the gif rotates around the 3D graph to clearly view the graph.

## Developers
Eamon Ito-Fisher
Andrew Mascillaro
