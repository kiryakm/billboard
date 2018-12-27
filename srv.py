from flask import Flask, render_template, request
from ftplib import FTP
import base64
import re
import os
import subprocess
import threading

from loader import *

app = Flask(__name__)

def Draw():
    Connect()
    ClearScreen(15)
    p = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
    path = list()
    for root, dirs, files in os.walk(p):
        for filename in files:
            path.append(p + filename)
    print(path[0])
    img = Image.open(path[0])
    width, height = img.size

    xCoord = 0
    yCoord = 0
    rotationAngle = 2  # 0-0 1-90 2-180 3-270
    wave = 2  # 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
    black = 0  # Черная корректировка значения: 0-15 в коде не использую если надо то можно добавить
    white = 0  # Белая корректировка значения: 0-15 в коде не использую если надо то можно добавить
    Partial = False
    Packed = True

    Load(path[0], xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed)



@app.route('/upload', methods=['GET', 'POST'])  #загрузка картинки
def upload():
    #получаю картинку в base64 и название картинки из принятого json
    img = request.json['data']
    name = request.json['name']
    #num = request.json['num']
    img = re.sub('data:image/png;base64,', '', img) #убираю лишнее из строки картинки
    with open("img/" + name + ".png", "wb") as fh:  #декодирую из base64 и сохраняю в папку img
        fh.write(base64.b64decode(img))
    return render_template("index2.html")

@app.route('/send', methods=['GET', 'POST'])  #загрузка картинки
def send():
    # Удаляю все содержимое папки в которую сохраняются картинки т.к. вывожу первую картинку в папке
    folder = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    print("sending")
    t = threading.Timer(3.0, Draw)  # через 3 секунд отправляю изображение на экран
    t.start()                       # таймер нужен что бы дождаться загрузки всех изображений
    print("send")

@app.route('/')
def index():
    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug = True)

