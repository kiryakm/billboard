import serial.tools.list_ports
import serial
import time
import sys
import os
from PIL import Image
import datetime


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


def Load(path, xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed):
    typeOfFile = path[-4:]

    DataPack = list()
    Image_Data = list()
    w = 0
    h = 0
    if typeOfFile == ".png":
        #print(typeOfFile)
        img = Image.open(path)
        w, h = img.size
        Image_Data = bytearray(img.tobytes())
    # Init Transfer parameters
    DataPack.clear()
    # Header Packet
    DataPack.append(0x88)
    DataPack.append(0x32)
    # CMD
    # Packed / UnPacked
    if Packed == True:
        DataPack.append(0x04)  # Packed
    else:
        DataPack.append(0x05)  # UnPacked

    if Partial == True:  # 7 bit // 0 - full update // 1 - Partial update
        full = 0x80
    else:
        full = 0x00
    DataPack.append(full | (rotationAngle << 4) | wave)
    #print(DataPack)

    def int_to_bytes(value, length):
        result = []
        for i in range(0, length):
            result.append(value >> (i * 8) & 0xff)
        return result

    widght = int_to_bytes(w, 2)
    widght_s = int_to_bytes(xCoord, 2)
    height = int_to_bytes(h, 2)
    height_s = int_to_bytes(yCoord, 2)

    # OERIG_X
    DataPack.append(widght_s[0])
    DataPack.append(widght_s[1])
    # OERIG_Y
    DataPack.append(height_s[0])
    DataPack.append(height_s[1])
    # WIDTH
    DataPack.append(widght[0])
    DataPack.append(widght[1])
    # HEIGHT
    DataPack.append(height[0])
    DataPack.append(height[1])

    SendData(DataPack)
    DataPack.clear()

    offset = 1
    if typeOfFile == ".png":
        offset = w * 7
    buff_r = [None] * w
    buff_g = [None] * w
    buff_b = [None] * w
    buff_w = [None] * w

    i = 0
    #print(len(Image_Data))
    while i < len(Image_Data) - offset:
        if Packed == True:
            if i < len(Image_Data) - offset:
                if typeOfFile == ".png":
                    for ii_ in range(w):
                        if rotationAngle == 0:
                            buff_r[ii_] = Image_Data[i + 0]
                            buff_g[ii_] = Image_Data[i + 2]
                            buff_b[ii_] = Image_Data[i + 1]
                            buff_w[ii_] = round(((((buff_r[ii_] & 0x00) >> 4) +
                                                  ((buff_g[ii_] & 0x00) >> 4) +
                                                  ((buff_b[ii_] & 0x00) >> 4)) / 3))
                        if rotationAngle == 1:
                            buff_r[ii_] = Image_Data[i + 1]
                            buff_g[ii_] = Image_Data[i + 0]
                            buff_b[ii_] = Image_Data[i + 2]
                            buff_w[ii_] = round(((((buff_r[ii_] & 0xFF) >> 4) +
                                                  ((buff_g[ii_] & 0xFF) >> 4) +
                                                  ((buff_b[ii_] & 0xFF) >> 4)) / 3))
                        if rotationAngle == 2:
                            buff_r[ii_] = Image_Data[i + 2]
                            buff_g[ii_] = Image_Data[i + 0]
                            buff_b[ii_] = Image_Data[i + 1]
                            buff_w[ii_] = round(((((buff_r[ii_] & 0xFF) >> 4) +
                                                  ((buff_g[ii_] & 0x00) >> 4) +
                                                  ((buff_b[ii_] & 0x00) >> 4)) / 3))
                            # buff_w[ii_] = round(((((buff_r[ii_] & 0x00) >> 4) +
                            #                       ((buff_g[ii_] & 0xFF) >> 4) +
                            #                       ((buff_b[ii_] & 0xFF) >> 4)) / 3))
                        if rotationAngle == 3:
                            buff_r[ii_] = Image_Data[i + 2]
                            buff_g[ii_] = Image_Data[i + 1]
                            buff_b[ii_] = Image_Data[i + 0]
                            buff_w[ii_] = round(((((buff_r[ii_] & 0xFF) >> 4) +
                                                  ((buff_g[ii_] & 0xFF) >> 4) +
                                                  ((buff_b[ii_] & 0xFF) >> 4)) / 3))

                        # buff_w[ii_] = round(((((buff_r[ii_] & 0xFF) >> 4) + ((buff_g[ii_] & 0xFF) >> 4) + ((buff_b[ii_] & 0xFF) >> 4)) / 3)+ (black) & ~(white))
                        i += 8

                    for ii_ in range(round(w / 2)):
                        DataPack.append((buff_r[ii_] & 0xF0) | ((buff_b[ii_] & 0xF0) >> 4))

                    for ii_ in range(round(w / 2)):
                        DataPack.append((((buff_w[ii_]) & 0x0F) << 4) | ((buff_g[ii_] & 0xF0) >> 4))
                        # DataPack.append((((buff_w[ii_]) & 0x0F) << 4) | ((buff_g[ii_] & 0xF0) >> 4))


        #else: Unpacked работает для .pgm формата я его не добавлял
        #if i % w == 0:
            # SendData(DataPack)
            # DataPack.clear()

    SendData(DataPack)
    DataPack.clear()
    DataPack.append(0x00)
    DataPack.append(0x00)
    SendData(DataPack)
    DataPack.clear()
    _port.close()



# Connect()
# ClearScreen(15)
# p = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
# path = list()
# for root, dirs, files in os.walk(p):
#     for filename in files:
#         path.append(p + filename)
# print(path[0])
# img = Image.open(path[0])
# width, height = img.size
#
# xCoord = 0
# yCoord = 0
# rotationAngle = 2   # 0-0 1-90 2-180 3-270
# wave = 2            # 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
# black = 0           # Черная корректировка значения: 0-15 в коде не использую если надо то можно добавить
# white = 0           # Белая корректировка значения: 0-15 в коде не использую если надо то можно добавить
# Partial = False
# Packed = True
#
# Load(path[0], 0, 0, rotationAngle, wave, black, white, Partial, Packed)
#
# # print(datetime.datetime.now())
# # y = 0
# # while y < 960:
# #     x = 0
# #     while x < 1280:
# #         Load(path[0], x, y, rotationAngle, wave, black, white, Partial, Packed)
# #         x += width
# #     y += height
# # print(datetime.datetime.now())