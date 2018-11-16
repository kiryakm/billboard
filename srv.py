from flask import Flask, render_template, request
import base64
import re

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])  #загрузка картинки
def upload():
    #получаю картинку в base64, название и номер картинки из принятого json
    img = request.json['data']
    name = request.json['name']
    #num = request.json['num']
    img = re.sub('data:image/png;base64,', '', img) #убираю лишнее из строки картинки
    with open("img/" + name + ".png", "wb") as fh:  #декодирую из base64 и сохраняю в папку img
        fh.write(base64.b64decode(img))
    return render_template("index.html")

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)