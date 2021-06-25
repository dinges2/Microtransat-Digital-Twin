'''
global sail is de zeil hoek ten opzichte van de wereld
local sail is de zeil hoek ten opzichte van de boot

'''

import simpylc as sp

class Sailboat (sp.Module):
    def __init__(self):
        sp.Module.__init__(self)
        #create the sailboat page that appears onscreen
        self.page('sailboat')

        self.group('transform', True)
        self.position_x = sp.Register()
        self.position_y = sp.Register()
        self.position_z = sp.Register()
        self.sailboat_rotation = sp.Register()

        self.group('body')
        self.mass = sp.Register(20)

        self.group('velocity')
        self.drag_deacceleration = sp.Register()
        self.acceleration = sp.Register()
        self.forward_velocity = sp.Register()
        self.horizontal_velocity = sp.Register()
        self.vertical_velocity = sp.Register()


        self.group('force')
        self.drag = sp.Register()
        self.head_wind_force = sp.Register()
        self.perpendicular_sail_force = sp.Register()
        self.forward_sail_force = sp.Register()
        self.apparent_wind_force = sp.Register()

        self.group('sail')
        self.target_sail_angle = sp.Register()
        self.local_sail_angle = sp.Register()
        self.global_sail_angle = sp.Register()
        self.angle_between_sail_and_apparent_wind = sp.Register()
        self.apparent_wind_angle = sp.Register()
        self.angle_between_course_and_true_wind = sp.Register()

        self.group('direction')
        self.boot_direction = sp.Register()
        self.head_wind_direction = sp.Register()
        self.apparent_wind_direction = sp.Register()
        
        self.group('rudder')
        self.target_gimbal_rudder_angle = sp.Register(0)
        self.gimbal_rudder_angle = sp.Register(0)
        self.rotation_speed = sp.Register()

        self.group('pause')
        self.pause = sp.Marker()

    #function to input the rotation of the rudder and sail
    def input(self):
        self.part('target sail angle')
        self.target_sail_angle.set(sp.world.control.target_sail_angle)
        
        self.part('gimbal rudder angle')
        self.target_gimbal_rudder_angle.set(sp.world.control.target_gimbal_rudder_angle)

        self.pause.mark(sp.world.control.pause)

    #function that is called every few seconds in world.py
    def sweep(self):
        self.local_sail_angle.set(self.local_sail_angle - 1, self.local_sail_angle > self.target_sail_angle)
        self.local_sail_angle.set(self.local_sail_angle + 1, self.local_sail_angle < self.target_sail_angle)
        self.global_sail_angle.set((self.sailboat_rotation + self.local_sail_angle + 180) % 360)

        self.gimbal_rudder_angle.set(self.gimbal_rudder_angle - 1,
                                     self.gimbal_rudder_angle > self.target_gimbal_rudder_angle)
        self.gimbal_rudder_angle.set(self.gimbal_rudder_angle + 1,
                                     self.gimbal_rudder_angle < self.target_gimbal_rudder_angle)

        if not self.pause:
            # Calculate forward force in N based on the angle between the sail and the wind
            self.angle_between_sail_and_apparent_wind.set(sp.abs(self.global_sail_angle - self.apparent_wind_direction) % 360)
            self.angle_between_sail_and_apparent_wind.set(sp.abs(180 - self.angle_between_sail_and_apparent_wind) % 360, self.angle_between_sail_and_apparent_wind > 90)
            self.angle_between_course_and_true_wind.set(sp.world.wind.wind_direction - self.sailboat_rotation)

            # Headforce = sail area * wind pressure
            # Wind pressure = 0.613 * wind speed ^ 2
            self.head_wind_force.set(2 * 0.613 * 2 * self.forward_velocity)

            # Calculate the apparent wind force
            self.apparent_wind_force.set(sp.sqrt(sp.world.wind.wind_scalar * sp.world.wind.wind_scalar + self.head_wind_force * self.head_wind_force + 2 * sp.world.wind.wind_scalar * self.head_wind_force * sp.cos(self.angle_between_course_and_true_wind)))
            
            # Calculate the angle between the head wind and the apparent wind
            self.apparent_wind_angle.set(sp.acos(round((sp.world.wind.wind_scalar * sp.cos(self.angle_between_course_and_true_wind) + self.head_wind_force) / self.apparent_wind_force, 2)))

            # Calculate the perpendicular force to the sail area
            self.perpendicular_sail_force.set(self.apparent_wind_force * sp.sin(self.angle_between_sail_and_apparent_wind))

            # Easy solution for sailing against the wind
            # If the sailboat is sailing against the wind then set the forward force to zero
            if self.apparent_wind_angle < 90 or self.apparent_wind_angle > 270:
                self.forward_sail_force.set(0)
            else:
                self.forward_sail_force.set(self.perpendicular_sail_force * sp.sin(self.local_sail_angle))

            self.forward_sail_force.set(sp.abs(self.forward_sail_force))

            # Easy and not 100% accurate drag calculation
            # See "drag documentation" for more information
            self.drag.set((0.83 * self.forward_velocity - 0.38))

            # Make sure drag = 0 when the sailboat is not sailing
            if self.drag < 0:
                self.drag.set(0)

            # Newton's second law
            self.drag_deacceleration.set(self.drag / self.mass)
            self.acceleration.set((self.forward_sail_force / self.mass) - self.drag_deacceleration)
            self.forward_velocity.set(sp.limit(self.forward_velocity + self.acceleration * sp.world.period, 20))

            # Splitting forward velocity vector into vertical and horizontal components
            self.vertical_velocity.set(sp.sin(self.sailboat_rotation) * self.forward_velocity)
            self.horizontal_velocity.set(sp.cos(self.sailboat_rotation) * self.forward_velocity)

            #update x y positions as well as the directions for the visualisation
            self.position_x.set(self.position_x + self.horizontal_velocity * 0.001)
            self.position_y.set(self.position_y + self.vertical_velocity * 0.001)
            self.rotation_speed.set(0.001 * self.gimbal_rudder_angle * self.forward_velocity)
            self.sailboat_rotation.set((self.sailboat_rotation - self.rotation_speed) % 360)

            self.boot_direction.set(180 + self.sailboat_rotation)
            self.head_wind_direction.set((self.boot_direction + 180) % 360)

            # Make sure the apparent wind direction is correct
            if sp.world.wind.wind_direction <= self.head_wind_direction:
                self.apparent_wind_direction.set((self.head_wind_direction - self.apparent_wind_angle) % 360)
            else:
                self.apparent_wind_direction.set((self.head_wind_direction + self.apparent_wind_angle) % 360)