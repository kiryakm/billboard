from flask import Flask, render_template, request
import base64
import re
import threading
import os

from Display import displayUSB as dispUSB
from Display import displaySSH as dispSSH

app = Flask(__name__)

host = '192.168.8.1'
user = 'debian'
pwd = 'temppwd'
port = 22

fromPath = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/" # Путь к директории с изображениями на этом устройстве
toPath = "/var/lib/cloud9/Projects/ver_0.2/ImageForPrint/"  # Путь к директории с изображениями на BeagleBone
script = "/var/lib/cloud9/Projects/ver_0.2/main.py" # Полный путь к скрипту на BeagleBone
xCoord = 0
yCoord = 0
rotationAngle = 0  # 0-0 1-90 2-180 3-270
wave = 2  # 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
black = 0  # Черная корректировка значения: 0-15 в коде не использую если надо то можно добавить
white = 0  # Белая корректировка значения: 0-15 в коде не использую если надо то можно добавить
Partial = False
Packed = True

def getFiles(fromPath):
    path = list()
    for root, dirs, files in os.walk(fromPath):
        for filename in files:
            path.append(fromPath + filename)
    return path

def getRotationAngle(file):
    if file[0: 3] == "ver":
        return 1
    else:
        return 0

def DrawSSH():
    '''
    Отправка изобраажений по SSH на BeagleBone
    и запуск скрипта для вывода на экран
    '''
    Display = dispSSH.DisplaySSH()

    path = getFiles(fromPath)
    rotationAngle = getRotationAngle(path[0])
    print(path[0])

    Display.repack(path[0], xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed)
    Display.sendSSH(fromPath, toPath, host, user, pwd, port)
    Display.ranScriptSSH(script, host, user, pwd, port)

def DrawUSB():
    '''
    Вывод изображения на экран, который подключен по USB
    Оставил на всякий случай
    '''
    Display = dispUSB.DisplayUSB()

    path = getFiles(fromPath)
    rotationAngle = getRotationAngle(path[0])
    print(path[0])
    binPath = path[0][0: -3] + "bin"

    Display.connect()
    Display.clearScreen(15)
    Display.repack(path[0], xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed)
    Display.load(binPath)

@app.route('/upload', methods=['GET', 'POST'])  # Получить изображения
def upload():
    # Получаю данные из принятого json
    img = request.json['data']  # Изображение в base64
    name = request.json['name'] # Название изображения
    img = re.sub('data:image/png;base64,', '', img)
    with open("img/" + name + ".png", "wb") as fh:  # Декодирую из base64 и сохраняю в папку img
        fh.write(base64.b64decode(img))
    return render_template("index2.html")

@app.route('/send', methods=['GET', 'POST'])  # Вывод изображения
def send():
    # Удаляю старое содержимое папки
    for file in os.listdir(fromPath):
        file_path = os.path.join(fromPath, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    t = threading.Timer(3.0, DrawSSH)   # через 3 секунды отправляю изображение на экран
    t.start()                           # таймер нужен что бы дождаться загрузки всех изображений
    return render_template("index2.html")

@app.route('/')
def index():
    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug = True)

