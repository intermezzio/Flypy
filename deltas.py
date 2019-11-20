def dveldtheta():
    '''
    gravity:
        dvdt = g

    lift:
        dvdt = sum(rotor_forces)/mass

    roll, pitch:
        for i in (frontback, leftright)
            force_one_way = front_forces - back_forces
            torque = force_one_way * distance
            alpha = torque / moment_of_inertia

            tilt = some_relation_to_that_force(current_rollpitch, force_one_way)

    yaw:
        rotor_angular_momentum = sum(L_from_F(rotors))
        dv_yaw = -rotor_angular_momentum / moment_of_inertia
        actual_dyaw = function_to_compare_rollpitchyaw(roll, pitch, dv_yaw, dt)



    '''
    pass
