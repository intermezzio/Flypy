import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi, sin, cos, tan, sqrt
import json
import sys

from drone import Drone

def goodRotorSpeeds(avg_speed, rollpitch=0, rollpitch_power=0, yaw_power=0):
    """
    Generate rotor speeds given a desired direction

    Parameters:
        avg_speed: The average rotor speed
        rollpitch: The angle (in radians bearing (0=N, pi/2=E, etc))
        rollpitch_power: How strong is the rollpitch
        yaw_power: The yaw angle (CW is positive)

    Returns:
        List: Rotor Speeds
    """
    rotor_tl = -rollpitch_power * cos(rollpitch + pi/4) # topleft
    rotor_tr = -rollpitch_power * cos(rollpitch - pi/4) # topright
    rotor_bl = -rollpitch_power * cos(rollpitch + 3*pi/4) # bottomleft
    rotor_br = -rollpitch_power * cos(rollpitch - 3*pi/4) # bottomright
    # print(f"rollpitch:\n[{rotor_tl}, {rotor_tr},\n {rotor_bl}, {rotor_br}]")
    r_speed = [avg_speed - yaw_power + rotor_tl, avg_speed + yaw_power + rotor_tr, 
               avg_speed + yaw_power + rotor_bl, avg_speed - yaw_power + rotor_br]
    return r_speed

def runDrone(drone, dx = 0, dy = 0, dz = 0):
    """
    Run a drone given a drone object and desired endpoint 
    
    Parameters:
        dx: change in x coordinate
        dy: change in y coordinate
        dz: change in z coordinate
    """
    sdDist = lambda x, y, z: sqrt(x**2 + y**2 + z**2)
    totDist = sdDist(dx, dy, dz)
    
    drone_props = pd.DataFrame(columns=["x", "y", "z",
        "vx", "vy", "vz", "roll", "pitch", "yaw", "time"])
    
    i = 0
    drone_props.loc[i] = drone.get_params()
    x, y, z, t = drone_props.loc[i, ["x", "y", "z", "time"]]
    z -= 10
    drDist = sdDist(x,y,z)

    while drDist < totDist and t < 10:
        i += 1
        drone.update(dt=0.05)
        drone_props.loc[i] = drone.get_params()

        x, y, z, t = drone_props.loc[i, ["x", "y", "z", "time"]]
        z -= 10 # drone starts 10m above ground
        drDist = sdDist(x,y,z)

    del drone
    dist = sdDist(dx-x, dy-y, dz-z)
    del drone_props
    return (x, y, z, t, dist)

def angleToCardinal(angle):
    """
    Given an angle (in radians), return the cardinal direction
    
    Parameters:
        angle: The angle (in radians)

    Returns:
        String: Cardinal direction
    """
    direction = int((angle + pi/8) // (pi/4))
    cardinals = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return cardinals[direction]

def cardinalToAngle(cardinal):
    """
    Given a direction, return the angle
    
    Parameters:
        cardinal: The direction

    Returns:
        Float: Angle (radians)
    """
    cardinals = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    indx = cardinals.index(cardinal)

    return pi/4 * indx

# Assign target drone coordinates
target_xyz = (3,3,3) if len(sys.argv) < 4 else [int(i) for i in sys.argv[1:4]]

def moveDrone(*target_xyz):
    """
    Given a target x, y, z find a rotor setting that gets the drone there
    Outputs results to a JSON
    
    Parameters:
        target_xyz: x, y, and z values (unpacked)

    Returns:
        Dict: nested dict with all tries and the optimal rotor setting

    """

    # Solutions is a nested dictionary
    solutions = dict()
    min_dist = np.inf

    # Min_props is a dicitonary for optimal settings
    min_props = dict()

    # Sweep through drone attributes
    for hover_spd in range(580, 740, 20):
        # Create nested dict
        solutions[hover_spd] = dict()
        print("hover_spd:", hover_spd)

        for angle in np.arange(0,2*pi, pi/4): # sweep 45 degrees at a time around in a circle

            c_angle = angleToCardinal(angle)
            solutions[hover_spd][c_angle] = dict()

            for rollpitch_power in (1, 5): # choose between a lot and a little roll/pitch
                solutions[hover_spd][c_angle][rollpitch_power] = dict()

                for yaw_power in (-1, 0, 1): # choose yaw and direction
                    thisCase = dict()

                    # Generate rotor speeds from properties
                    r_speed = goodRotorSpeeds(hover_spd, rollpitch=angle, 
                              rollpitch_power=rollpitch_power, yaw_power=yaw_power)
                    
                    # Create drone and model it
                    drone = Drone(r_speed=r_speed)
                    x, y, z, t, dist = runDrone(drone, *target_xyz)
                    
                    # Store values
                    thisCase["x"], thisCase["y"], thisCase["z"] = x, y, z
                    thisCase["t"], thisCase["dist"] = t, dist
                    
                    # if optimal solution
                    if thisCase["dist"] < min_dist:
                        min_props = {
                            "hover_spd": hover_spd,
                            "c_angle": c_angle,
                            "angle": angle,
                            "rollpitch_power": rollpitch_power,
                            "yaw_power": yaw_power,
                            "min_dist": thisCase["dist"],
                            "x": thisCase["x"],
                            "y": thisCase["y"],
                            "z": thisCase["z"]
                        }
                        min_dist = thisCase["dist"]
                    solutions[hover_spd][c_angle][rollpitch_power][yaw_power] = thisCase

    # Create full dictionary
    full_dict = {
        "tries": solutions,
        "key": min_props
    }

    # Write to JSON
    with open(f"x{target_xyz[0]}y{target_xyz[1]}z{target_xyz[2]}.json", "w") as js:
        json.dump(full_dict, js, indent=4, sort_keys=True)

    return full_dict


if __name__ == "__main__":
    print(moveDrone(*target_xyz)["key"])
