# -*- coding: utf-8 -*-
import math

class Joystick:
    def __init__(self, data):
        self.force = data.get('forca', 0)
        self.angle = data.get('angulo', 0)

    def __str__(self):
        return u'Force: %.2f | Angle: %d°' % (self.force, self.angle)

    @property
    def direction_vector(self):
        radians = math.radians(self.angle)
        x = math.cos(radians)
        y = math.sin(radians)
        print("Angle: ", self.angle, " | X: ", x, " | Y: ", y)
        return x, y

    @property
    def is_max_force(self):
        return self.force == 1

    @property
    def is_using(self):
        return self.force == 0