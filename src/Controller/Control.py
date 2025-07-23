# -*- coding: utf-8 -*-
import urllib2
import json
import time
from JoyStick import Joystick

class Control(object):
    def __init__(self, nao):
        self.__server_url = 'http://localhost:8090/control'
        self.__left_joystick = None
        self.__right_joystick = None
        self.__nao = nao
        self.__running = True
        self.__last_obstacle_time = 0

    def __fetch_joystick_data(self):
        """Método para obter dados do joystick"""
        try:
            response = urllib2.urlopen(self.__server_url)
            data = json.load(response)
            self.__left_joystick = Joystick(data.get('esquerdo', {}))
            self.__right_joystick = Joystick(data.get('direito', {}))
        except Exception, e:
            print("Erro ao obter dados do joystick: {}".format(e))
            raise

    def breakAll(self):
        self.__running = False

    def start(self):
        self.__nao.start()
        while self.__running:
            try:
                self.__fetch_joystick_data()

                x_right, y_right = 0.0, 0.0
                x_left, y_left = 0.0, 0.0
                
                if self.__right_joystick and not self.__right_joystick.is_using:
                    x_right, y_right = self.__right_joystick.direction_vector
                    
                    # Reduz velocidade se obstáculo detectado recentemente
                    if time.time() - self.__last_obstacle_time < 3:
                        x_right *= 0.7
                        y_right *= 0.7

                if self.__left_joystick and not self.__left_joystick.is_using:
                    x_left, y_left = self.__left_joystick.direction_vector

                # Verificar obstáculos com movimento inteligente
                if getattr(self.__nao, '_NAO__obstacle_detected', False):
                    # Se estiver tentando ir PARA FRENTE (y_right > 0), bloqueia
                    if y_right > 0.1:  # Limiar de sensibilidade
                        self.__nao.move(0.0, 0.0)  # Para movimento frontal
                        self.speak("Obstacle ahead")
                    # Permite movimento para trás ou laterais
                    elif y_right < -0.1 or abs(x_right) > 0.1:
                        self.__nao.move(x_right, y_right)  # Permite recuar ou girar
                    self.__last_obstacle_time = time.time()
                else:
                    # Movimento normal sem obstáculos
                    self.__nao.move(x_right, y_right)
                    self.__nao.look(x_left, y_left)

                time.sleep(0.05)

            except Exception, e:
                print("Erro no loop principal: {}".format(e))
                time.sleep(1)