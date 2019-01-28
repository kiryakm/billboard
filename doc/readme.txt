Структура проекта: 
srv.py - основной файл сервера
templates/index2.html - страница с интерфейсом
static/css/ - файлы с css
statick/js/ - файлы с javascript
в img сохраняются изображения
в doc документация
в Display python файлы реализующие классы для вывода изображений

Класс DisplaySSH используется для вывода изображения по SSH
Функции:
repack(self, path, xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed)
Конвертирует из png в bin
сохраняет в директорию в которой оригинал
path: путь к изображению
rotationAngle: 0-0 1-90 2-180 3-270
wave: 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
black: Черная корректировка значения: 0-15
white:  Белая корректировка значения: 0-15

sendSSH(self, fromPath, toPath, host, user, pwd, port)
Отправляет по SSH все содержимое директории fromPath на хост в toPath
pwd: пароль

ranScriptSSH(self, script, host, user, pwd, port)
Запускает скрипт на хосте
pwd: пароль

Класс DisplayUSB используется для вывода изображения на экран , который подключен по USB
Функции:
connect(self)
Подключиться через com порт

sendData(self, data)
data: Отправляемые данные

clearScreen(self, colorUpDown)
colorUpDown: каким цветом закрасить: 0-черный, 15 - белый

load(self, path)
Вывести изображение на экран
path: путь к изображению закодированному в bin

repack(self, path, xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed)
Конвертирует из png в bin
сохраняет в директорию в которой оригинал
path: путь к изображению
rotationAngle: 0-0 1-90 2-180 3-270
wave: 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
black: Черная корректировка значения: 0-15
white:  Белая корректировка значения: 0-15

Функции конвертирования для SSH и USB отличаются тем, что по разному создают header


Функции JavaScript:
canvasDown(ev), canvasUp(ev), mouseMove(ev) - обработчики для клика и движения мыши по canvas-у с оригинальным изображением

redraw(x, y)- отрисовка при двежение мыши
x и y - координаты на которых ЛКМ была отпущена
Высчитывает множители по X и Y(multX, multY)

rotate() - перевернуть изображение по часовой стрелке

getId(i, j, inum, jnum) - получить Id canvas-а. 
i, j - номер canvas-a
inum -количество canvas-ов по вертикали
jnum - по горизонтали. Возвращает Id

getName(pic, i, j, inum, jnum) - получить название изображения для отправки на сервер. 
pic - оригинальное изображение 
Возвращает название

rotateCtx(canvas) - повернуть контекст canvas-a
canvas - canvas контекст которого надо повернуть
Возвращает контекст

drawOriginal(multX, multY) - отрисовка оригинального изображения 
multX, multY - множители по X и Y

stretchOrigX () - растянуть оригинальное изображение по X

stretchOrigY () - растянуть оригинальное изображение по Y

stretchPrevX () - растянуть изображение на экранах по X
Задает mode = 1 mode - это способ отрисовки изображения на экранах: 
1 - растягиваем по X, 2 - по Y, 3 - растягиваем до максимума, 0 - обычная отрисовка

stretchPrevY () - растянуть изображение на экранах по Y
Задает mode = 2

stretchPrevXY () - максимально растянуть изображение на экранах
Задает mode = 3

setScreenDiv(inum, jnum) - получить делитель экранов для отображения
inum - количество canvas-ов по вертикали
jnum - по горизонтали

getInf(height, width, inum, jnum) - Получить информацию о изображении и экранах для вывода на экран. 
height - высота экранов 
width - ширина экранов
inum -количество canvas-ов по вертикали
jnum - по горизонтали

getHW() - возвращает высоту и ширину экранов

makeTable(multX, multY) - создать таблицу для отрисовки
multX, multY - множители по X и Y

draw(multX, multY) - начать отрисовку изображения на экранах
multX, multY - множители по X и Y

drawing(canvas, pic, sumW, sumH, inum, jnum, multX, multY, screenDiv, height, width, mode) - сама отрисовка. 
canvas - canvas на котором рисуем. 
sumW, sumH - смещение отрисовки по X и Y соответственно. 
screenDiv - делитель размера экранов. 
height - высота экранов width - ширина экранов. 
mode - способ отрисовки изображения на экранах.

send() - увеличивает canvas-ы до оригинального разрешения(1280x960), отрисовывает в них изображение оригинального разрешения, 
кодирует содержимое canvas-a в base64, отправляет на сервер и затем отрисовывает обратно.

upload(dataURL, name) - функция с ajax запросом для отправки изображения на сервер
dataURL - изображение закодированное в base64, 
name - название изображения