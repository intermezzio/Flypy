
import numpy as np

class Vector:

    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 1/2

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def dotP(self, v2):
        self.x *= v2.x
        self.y *= v2.y
        self.z *= v2.z
        return

    def cross_product(self, v2):
        x = self.y * v2.z - self.z * v2.y
        y = self.z * v2.x - self.x * v2.z
        z = self.x * v2.y - self.y * v2.x
        return Vector(x=x, y=y, z=z)

    def numpy(self):
        return np.array([self.x, self.y, self.z])
    
    def from_numpy(self, arry):
        self.x = arry[0]
        self.y = arry[1]
        self.z = arry[2]
