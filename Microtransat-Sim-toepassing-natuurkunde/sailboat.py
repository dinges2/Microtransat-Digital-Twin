# TODO: Refactor and document
# Wat is de hoek van de wind ten opzichten van de x-as, tegen de klok is positief
# Wat is de gewenste koershoek
# Wat is het hoekverschil tussen de gewenste koershoek en de windhoek
# Wat is de zeilstand (helft van stap 3)
# Wat is de component van de wind die effect heeft op het zeil
# loodrecht = totale windkracht * sin (alpha)
# voorwaards = loodrecht * cos (beta)
# beta = 90 - hoek van het zeil met de boot

'''
global sail is de zeil hoek ten opzichte van de wereld
local sail is de zeil hoek ten opzichte van de boot


'''


import simpylc as sp
# import data.data
# TODO: better naming
def is_between_angles(n, a, b):
    if a < b:
        return a <= n <= b
    return a <= n or n <= b

def is_sailing_against_wind(min_threshold,
                            max_threshold,
                            local_sail_angle,
                            global_sail_angle,
                            wind_direction):
    if local_sail_angle < 0 and \
            global_sail_angle < min_threshold and not \
            is_between_angles(global_sail_angle, min_threshold, wind_direction):
        return True

    if local_sail_angle < 0 and \
            global_sail_angle > min_threshold and \
            is_between_angles(min_threshold, global_sail_angle, wind_direction):
        return True

    if local_sail_angle > 0 and \
            global_sail_angle < max_threshold and \
            is_between_angles(global_sail_angle, max_threshold, wind_direction):
        return True

    if local_sail_angle > 0 and \
            global_sail_angle > max_threshold and not \
            is_between_angles(max_threshold, global_sail_angle, wind_direction):
        return True
    return False


class Sailboat (sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page('sailboat')

        self.group('transform', True)
        self.position_x = sp.Register()
        self.position_y = sp.Register()
        self.position_z = sp.Register()
        self.sailboat_rotation = sp.Register()

        self.group('body')
        self.mass = sp.Register(20)

        self.group('velocity')
        self.drag = sp.Register()
        self.drag_deacceleration = sp.Register()
        self.acceleration = sp.Register()
        self.forward_velocity = sp.Register()
        self.horizontal_velocity = sp.Register()
        self.vertical_velocity = sp.Register()

        self.group('sail')
        self.target_sail_angle = sp.Register()
        self.local_sail_angle = sp.Register()
        self.global_sail_angle = sp.Register()
        self.sail_alpha = sp.Register()
        self.perpendicular_sail_force = sp.Register()
        self.forward_sail_force = sp.Register()
        self.apparent_wind = sp.Register()
        self.apparent_wind_angle = sp.Register()
        self.boot_wind = sp.Register()
        self.alfa = sp.Register()
        
        self.group('rudder')
        self.target_gimbal_rudder_angle = sp.Register(0)
        self.gimbal_rudder_angle = sp.Register(0)
        self.rotation_speed = sp.Register()

        self.group('pause')
        self.pause = sp.Marker()

    def input(self):
        self.part('target sail angle')
        self.target_sail_angle.set(sp.world.control.target_sail_angle)
        
        self.part('gimbal rudder angle')
        self.target_gimbal_rudder_angle.set(sp.world.control.target_gimbal_rudder_angle)

        self.pause.mark(sp.world.control.pause)

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
            self.sail_alpha.set(sp.abs(self.global_sail_angle - sp.world.wind.wind_direction) % 360)
            self.sail_alpha.set(sp.abs(180 - self.sail_alpha) % 360, self.sail_alpha > 90)
            self.boot_wind.set(self.forward_velocity)
            self.alfa.set(abs(sp.world.wind.wind_direction - self.sailboat_rotation)%360)

            #bereken de kracht van de apparent wind door de echte wind te gebruiken en de rotatie van de boot
            self.apparent_wind.set(sp.sqrt(sp.world.wind.wind_scalar * sp.world.wind.wind_scalar + self.boot_wind * self.boot_wind + 2 * sp.world.wind.wind_scalar * self.boot_wind * sp.cos(self.alfa)))
            
            #bereken de hoek van de apparent wind aan de hand van de echte wind en de rotatie van de boot
            self.apparent_wind_angle.set(abs(sp.acos(((sp.world.wind.wind_scalar * sp.cos(self.alfa))+ self.forward_velocity)  / self.apparent_wind))%360)

            self.perpendicular_sail_force.set(self.apparent_wind * sp.sin(self.sail_alpha))
            self.forward_sail_force.set(self.perpendicular_sail_force * sp.sin(self.local_sail_angle))
            self.forward_sail_force.set(sp.abs(self.forward_sail_force))
            self.drag.set((0.83 * self.forward_velocity - 0.38))
            if self.drag < 0:
                self.drag.set(0)
            # Sailing against wind
            min_threshold = (self.global_sail_angle - 180) % 360
            max_threshold = (self.global_sail_angle + 180) % 360
            self.forward_sail_force.set(self.forward_sail_force,
                                        is_sailing_against_wind(min_threshold,
                                                                max_threshold,
                                                                self.local_sail_angle,
                                                                self.global_sail_angle,
                                                                sp.world.wind.wind_direction))

            # Newton's second law
            self.drag_deacceleration.set(self.drag / self.mass)
            self.acceleration.set((self.forward_sail_force / self.mass) - self.drag_deacceleration)
            self.forward_velocity.set(sp.limit(self.forward_velocity + self.acceleration * sp.world.period, 20))

            # Splitting forward velocity vector into vertical and horizontal components
            self.vertical_velocity.set(sp.sin(self.sailboat_rotation) * self.forward_velocity)
            self.horizontal_velocity.set(sp.cos(self.sailboat_rotation) * self.forward_velocity)

            self.position_x.set(self.position_x + self.horizontal_velocity * 0.001)
            self.position_y.set(self.position_y + self.vertical_velocity * 0.001)
            self.rotation_speed.set(0.001 * self.gimbal_rudder_angle * self.forward_velocity)
            self.sailboat_rotation.set((self.sailboat_rotation - self.rotation_speed) % 360)