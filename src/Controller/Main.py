# -*- coding: utf-8 -*-
from Control import Control
from NAO import NAO
import threading

IP_NAO = "127.0.0.2"

if __name__ == '__main__':
    nao = NAO(IP_NAO)
    control = Control(nao)

    control_thread = threading.Thread(target=control.start)
    camera_thread = threading.Thread(target=nao.show_camera)

    control_thread.start()
    camera_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nInterrompido com Ctrl+C!")
        control.breakAll()
        nao.breakAll()
