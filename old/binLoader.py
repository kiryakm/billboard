import serial.tools.list_ports
import serial
import time
import sys
import os


_port = serial.Serial()


def Connect():
    ports = list(serial.tools.list_ports.comports())  # Получаем порты
    portName = str(ports[0]).split(" ")[0]  # Берем из полученного только название
    global _port
    try:
        if (_port.is_open):
            _port.setRTS(False)
            _port.setDTR(False)
            _port.close()
            time.sleep(250)
        _port.baudrate = 9600
        _port.port = portName
        _port.setRTS(True)
        _port.setDTR(True)
        _port.timeout = None
        _port.parity = serial.PARITY_SPACE
        _port.open()
        print(_port)

    except Exception:
        print("Ошибка открытия СОМ порта\n")
        sys.exit()

def SendData(data):
    if data == None:
        print("Data is none")
        return
    if len(data) < 1:
        print("No data")
        return
    if _port == None:
        print("Port is none")
        return
    if _port.is_open == False:
        print("Port is close")
        return
    values = bytearray(data)
    _port.write(values)


def ClearScreen(colorUpDown):
    DataPack = list()
    DataPack.append(0x88)
    DataPack.append(0x32)
    DataPack.append(0x03)
    DataPack.append(colorUpDown)
    DataPack.append(0x00)
    DataPack.append(0x00)
    SendData(DataPack)


def Load(path):
    DataPack = list()
    with open(path, 'rb') as bin:
        i = 0
        while i<12:
            current_byte = bin.read(1)
            if (not current_byte):
                break
            DataPack.append(ord(current_byte))
            i+=1
        SendData(DataPack)
        DataPack.clear()
        while True:
            current_byte = bin.read(1)
            if (not current_byte):
                break
            DataPack.append(ord(current_byte))
        SendData(DataPack)
        DataPack.clear()
        DataPack.append(0x00)
        DataPack.append(0x00)
        SendData(DataPack)
        DataPack.clear()
        _port.close()

Connect()
ClearScreen(15)
p = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
path = list()
for root, dirs, files in os.walk(p):
    for filename in files:
        if filename[-3:] == "bin":
            path.append(p + filename)
print(path[0])

xCoord = 0
yCoord = 0
rotationAngle = 0   # 0-0 1-90 2-180 3-270
wave = 2            # 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
black = 0           # Черная корректировка значения: 0-15 в коде не использую если надо то можно добавить
white = 0           # Белая корректировка значения: 0-15 в коде не использую если надо то можно добавить
Partial = False
Packed = True

Load(path[0])
