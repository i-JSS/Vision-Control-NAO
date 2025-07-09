# -*- coding: utf-8 -*-
import urllib2
import json
from JoyStick import Joystick

class Control(object):
    def __init__(self, nao):
        self.__server_url = 'http://localhost:8090/control'
        self.__left_joystick = None
        self.__right_joystick = None
        self.__nao = nao
        self.__running = True

    def __fetch_joystick_data(self):
        response = urllib2.urlopen(self.__server_url)
        data = json.load(response)
        self.__left_joystick = Joystick(data.get('esquerdo', {}))
        self.__right_joystick = Joystick(data.get('direito', {}))

    def breakAll(self):
        self.__running = False

    def start(self):
        self.__nao.start()
        while self.__running:
            try:
                self.__fetch_joystick_data()

                x_right, y_right = 0, 0
                x_left, y_left = 0, 0
                if not self.__right_joystick.is_using:
                    x_right, y_right = self.__right_joystick.direction_vector

                if not self.__left_joystick.is_using:
                    x_left, y_left = self.__left_joystick.direction_vector


                self.__nao.move(x_right, y_right)
                self.__nao.look(x_left, y_left)


            except Exception as e:
                print("Failed to retrieve joystick data: %s" % str(e))
