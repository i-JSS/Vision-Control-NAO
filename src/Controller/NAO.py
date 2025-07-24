# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
from naoqi import ALProxy

class NAO():
    def __init__(self, ip, port=9559):
        self.ip = ip
        self.port = port
        self.__motion = ALProxy("ALMotion", ip, port)
        self.__speak = ALProxy("ALTextToSpeech", ip, port)
        self.__video_proxy = ALProxy("ALVideoDevice", ip, port)
        self.__memory = ALProxy("ALMemory", ip, port)
        self.__sonar = ALProxy("ALSonar", ip, port)
        self.__running = True
        self.__obstacle_detected = False
        self.__safe_distance = 0.5  # Distância segura em metros

    def start(self):
        print("Ligando NAO")
        self.__motion.wakeUp()

    def stop(self):
        print("Desligando NAO")
        self.__motion.rest()

    def speak(self, text):
        print("Ativando Fala NAO")
        self.__speak.say(text)

    def move(self, x, y, theta=0.0):
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

    def enable_sonar(self):
        """Ativa os sensores de sonar do NAO"""
        self.__sonar.subscribe("NAO_Sonar")
        print("Sonar ativado")

    def disable_sonar(self):
        """Desativa os sensores de sonar"""
        self.__sonar.unsubscribe("NAO_Sonar")
        print("Sonar desativado")

    def check_for_obstacles(self):
        """Verifica obstáculos usando os sonares"""
        try:
            left = self.__memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            right = self.__memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            
            # Considera o menor valor entre os dois sonares
            distance = min(left, right)
            
            if distance < self.__safe_distance:
                self.__obstacle_detected = True
                return True, distance
            else:
                self.__obstacle_detected = False
                return False, distance
        except Exception, e:
            return False, float('inf')

    def detect_objects(self, frame):
        """Detecta objetos usando visão computacional"""
        # Converter para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplicar desfoque para reduzir ruído
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        
        # Detecção de bordas
        edges = cv2.Canny(blurred, 30, 150)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos por área
        min_area = 500  # Ajuste conforme necessário
        large_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        return len(large_contours) > 0, frame

    def show_camera(self):
        camera = 1
        resolution = 0
        colorSpace = 11
        fps = 30
        clientName = "python_client"
        try:
            client = self.__video_proxy.subscribeCamera(clientName, camera, resolution, colorSpace, fps)
            self.enable_sonar()

            cv2.namedWindow("NAO Camera - FULLSCREEN", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("NAO Camera - FULLSCREEN", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            while self.__running:
                # Verificar obstáculos com sonar
                obstacle_sonar, distance = self.check_for_obstacles()
                
                naoImage = self.__video_proxy.getImageRemote(client)
                if not naoImage:
                    break

                width = naoImage[0]
                height = naoImage[1]
                imageArray = np.frombuffer(naoImage[6], dtype=np.uint8).reshape((height, width, 3))

                # Verificar obstáculos com visão computacional
                obstacle_vision, processed_frame = self.detect_objects(imageArray)
                
                # Se obstáculo detectado, parar o movimento
                if obstacle_sonar or obstacle_vision:
                    self.__motion.stopMove()
                    if not self.__obstacle_detected:
                        self.speak("Obstacle detected!")
                        self.__obstacle_detected = True
                else:
                    self.__obstacle_detected = False

                # Adicionar informações na imagem (formatado para Python 2.7)
                cv2.putText(processed_frame, "Sonar Distance: %.2fm" % distance, (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                obstacle_text = "OBSTACLE!" if self.__obstacle_detected else "CLEAR"
                obstacle_color = (0, 0, 255) if self.__obstacle_detected else (0, 255, 0)
                cv2.putText(processed_frame, obstacle_text, (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, obstacle_color, 2)

                tela_cheia = cv2.resize(processed_frame, (1920, 1080), interpolation=cv2.INTER_LINEAR)
                cv2.imshow("NAO Camera - FULLSCREEN", tela_cheia)
                cv2.waitKey(1)

        except Exception, e:
            print("Erro: {}".format(e))
        finally:
            self.disable_sonar()
            if 'videoProxy' in locals() and 'client' in locals():
                self.__video_proxy.unsubscribe(client)
            cv2.destroyAllWindows()
            print("Streaming encerrado.")