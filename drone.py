from vector import Vector
from math import pi, cos, sin

class Drone():
    """
    Drone class.

    Attributes:
        yaw: The yaw of the drone
        pitch: The pitch of the drone
        roll: The roll of the drone
        pos: Current drone position as a vector
        velocity: Current velocity of the drone as a vector
        r_speed: List of rotor speeds where index 0 is top left, index 1 if top
        right, index 2 is bottom left and index 3 is bottom right
                 Ex: [10, 9, 5, 8] is 10   09
                                         x
                                      05   08
        r: Radius of the drone rotors in m
        weight: Weight of the drone in g
        size: Size of the drone in m
        m_of_i: Moment of inertia of the drone
    """
    def __init_(self,
                rotor_radius=15,
                weight=50,
                size=10,
                m_of_i=1,
                r_m_of_i=1):
        """
        Constructor.

        Parameters:
            rotor_radius: Radius of the drone rotors in m
            weight: Weight of the drone in g
            size: Size of the drone in m
            m_of_i: Moment of inertia of the drone
            r_m_of_i: Moment of inertia of one rotor
        """
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.pos = Vector()
        self.velocity = Vector()
        self.r_speed = [0, 0, 0, 0]

        self.r = rotor_radius
        self.weight = weight
        self.size = size
        self.m_of_i = m_of_i
        self.r_m_of_i = r_m_of_i


    def change_rotor_speed(r_speed):
        """
        Changes the speeds of the four rotors as necessary

        Parameters:
            r_speed: Array of all four rotor speeds
        """
        if len(r_speed) == 4:
            self.r_speed = r_speed

    def update(self, dt=1, g=-9.81, r_speed=None):
        """
        Calculate the change in each positional variable and apply them

        Parameters:
            dt: Timestep size
            g: Force due to gravity
            r_speed: Array of all four rotor speeds
        """
        # Update rotor speeds if necessary
        if r_speed is not None:
            change_rotor_speed(r_speed)

        # Calculate acceleration in all 3 axis
        thrust = self.calc_thrust()
        gravity = Vector(0, 0, g)
        total_force = thrust + gravity
        acceleration = total_force / self.weight

        # Calculate change in rotations
        roll = self.calc_rotation(self.r_speed[0], self.r_speed[3])
        pitch = self.calc_rotation(self.r_speed[1], self.r_speed[2])
        yaw = self.calc_yaw()

        # Apply deltas
        self.pos += self.velocity * dt
        self.velocity += acceleration * dt
        self.roll += roll * dt
        self.pitch += pitch * dt
        self.yaw += yaw * dt

    def calc_thrust(self):
        """
        Calculates the thrust given current yaw / pitch / roll and returns a
        force vector.

        Returns:
            Vector: Force vector generated by the thrust of the rotors
        """
        # Calculate the upwards force due to the rotors.
        # See this answer for reference: https://aviation.stackexchange.com/a/16550
        total_force = sum([self.calc_rotor_force(s) for s in self.r_speed])

        # Rotate the initial force vector that is only in the Z direction by the
        # roll / pitch / yaw.
        # See this answer for reference: https://math.stackexchange.com/a/1637853
        force_matrix = np.array([[0], [0], [total_force]])
        roll_matrix = np.array([[cos(self.roll), 0, -sin(self.roll)],
                               [0, 1, 0],
                               [sin(self.roll), 0, cos(self.roll)]])
        force_matrix = np.matmul(roll_matrix, force_matrix)
        pitch_matrix = np.array([[1, 0, 0],
                                [0, cos(self.pitch), -sin(self.pitch)],
                                [0, sin(self.pitch), cos(self.pitch)]])
        force_matrix = np.matmul(pitch_matrix, force_matrix)
        yaw_matrix = np.array([[cos(self.yaw), sin(self.yaw), 0],
                              [-sin(self.yaw), cos(self.yaw), 0],
                              [0, 0, 1]])
        force_matrix = np.matmul(yaw_matrix, force_matrix)

        thrust = Vector(force_matrix[0], force_matrix[1], force_matrix[2])
        return thrust

    def calc_rotation(self, front_speed, back_speed):
        """
        Calculates the change in rotation in a direction given the speeds of opposing
        rotors

        Parameters:
            front_speed: The rotor speed of the front rotor of the pair being
            evaluted
            back_speed: The rotor speed of the back rotor of the pair being
            evaluted

        Returns:
            float: Rotation caused by the rotor pair
        """
        front_force = self.calc_rotor_force(front_speed)
        back_force = self.calc_rotor_force(back_speed)
        total_force = front_force - back_force

        torque = total_force * self.size / 2
        rotation = torque / self.m_of_i

        return rotation

    def calc_yaw(self):
        """
        Calculate the change in yaw

        Returns:
            float: Change in yaw given current rotor speeds
        """
        angular_momentum = [self.r_m_of_i * s for s in self.r_speed]
        # Get correct directions for angular momentum
        angular_momentum *= [1, -1, 1, -1]

        total_angular_momentum = sum(angular_momentum)
        rotation = total_angular_momentum / self.m_of_i

        return rotation

    def calc_rotor_force(self, speed, drag_coef=0.05, air_density=1.225):
        """
        Calculate the force of a rotor given a rotor speed.

        Parameters:
            speed: Speed of the rotor
            drag_coef: Drag coefficent of the rotors
            air_density: Density of the air

        Returns:
            float: Force generated by the rotor at the given speed
        """
        return drag_coef * air_density * pi * self.r ** 3 * speed

    def get_params(self):
        """
        Returns all positional attributes in a list

        Returns:
            list: Contains all positional parameters of the drone
        """
        params = [self.pos.x,
                  self.pos.y,
                  self.pos.z,
                  self.velocity.x,
                  self.velocity.y,
                  self.velocity.z,
                  self.roll,
                  self.pitch,
                  self.yaw]
        return params
