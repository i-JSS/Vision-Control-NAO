# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
from naoqi import ALProxy


class NAO():
    def __init__(self, ip, port = 9559):
        self.ip = ip
        self.port = port
        self.__motion = ALProxy("ALMotion", ip, port)
        self.__speak = ALProxy("ALTextToSpeech", ip, port)
        self.__video_proxy = ALProxy("ALVideoDevice", ip, port)
        self.__running = True

    def start(self):
        print("Ligando NAO")
        self.__motion.wakeUp()

    def stop(self):
        print("Desligando NAO")
        self.__motion.rest()

    def speak(self, text):
        print("Ativando Fala NAO")
        self.__speak.say(text)

    def move(self, x, y, theta = 0.0):
        self.__motion.move(y, x, theta)

    def look(self, x, y):
        inverted_x = -x
        inverted_y = -y

        HEAD_YAW_MIN = -2.0857
        HEAD_YAW_MAX = 2.0857
        HEAD_PITCH_MIN_GLOBAL = -0.6720
        HEAD_PITCH_MAX_GLOBAL = 0.5149

        clamped_x = max(min(inverted_x, HEAD_YAW_MAX), HEAD_YAW_MIN)
        if abs(clamped_x) < 0.1:
            pitch_min = HEAD_PITCH_MIN_GLOBAL
            pitch_max = HEAD_PITCH_MAX_GLOBAL
        else:
            pitch_min = -0.5
            pitch_max = 0.3

        clamped_y = max(min(inverted_y, pitch_max), pitch_min)

        self.__motion.setAngles("HeadYaw", clamped_x, 0.1)
        self.__motion.setAngles("HeadPitch", clamped_y, 0.1)

    def breakAll(self):
        self.__running = False
        self.stop()

    def show_camera(self):
        camera = 1
        resolution = 0
        colorSpace = 11
        fps = 30
        clientName = "python_client"
        try:
            client = self.__video_proxy.subscribeCamera(clientName, camera, resolution, colorSpace, fps)

            cv2.namedWindow("NAO Camera - FULLSCREEN", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("NAO Camera - FULLSCREEN", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            while self.__running:

                naoImage = self.__video_proxy.getImageRemote(client)
                if not naoImage:
                    break

                width = naoImage[0]
                height = naoImage[1]
                imageArray = np.frombuffer(naoImage[6], dtype=np.uint8).reshape((height, width, 3))

                tela_cheia = cv2.resize(imageArray, (1920, 1080), interpolation=cv2.INTER_LINEAR)

                cv2.imshow("NAO Camera - FULLSCREEN", tela_cheia)
                cv2.waitKey(1)


        except Exception as e:
            print("Erro:", e)
        finally:
            if 'videoProxy' in locals() and 'client' in locals():
                self.__video_proxy.unsubscribe(client)
            cv2.destroyAllWindows()
            print("Streaming encerrado.")
