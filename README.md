# Vision-Control-NAO & Obstacle Avoidance

![Python](https://img.shields.io/badge/Python_2.7-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NAO Robot](https://img.shields.io/badge/NAO_Robot-NAOqi-informational?style=for-the-badge)


![Exemplo NAO andando](images/output2.gif)

![Exemplo NAO curva](images/output.gif)


|             Aluno             | Matrícula |
|:-----------------------------:|:---------:|
| Leticia Miti Takahashi | 231035437  |
| João Antonio Ginuino carvalho | 221008150 |
| Marcos Antonio Teles de Castilhos | 221008300 |
| Diego Carlito Rodrigues de Souza | 221007690 |

---

## Instalação

Linguagem: Python - 2.7 | node 17+

Biblioteca: numpy, opencv e naoqi

> Instalador do NAOQI:

````bash
sudo apt install curl
curl https://raw.githubusercontent.com/i-JSS/Vision-Control-NAO/refs/heads/master/instalador.sh | sh
rm instalador.sh
````

> Instalando dependências (numpy e opencv):
````bash
pyenv activate UnBeatables
pip2 install opencv-python==4.2.0.32
pip2 install numpy
````

---

## Uso


Front: entrar em src > View e digitar:

````bash
node server.js
````

Abrir outro terminal

Back: entrar em src > Controller e digitar:

````bash
naopy Main.py
````
