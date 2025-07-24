# Vision-Control-NAO & Obstacle Avoidance


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
