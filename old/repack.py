import os
from PIL import Image


def Repack(path, xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed):
    DataPack = list()
    Image_Data = list()
        
    typeOfFile = path[-4:]
    binPath = path[0: -3] + "bin"
    print(path)

    f = open(binPath, "wb")

    w = 0
    h = 0
    if typeOfFile == ".png":
        #print(typeOfFile)
        img = Image.open(path)
        w, h = img.size
        Image_Data = bytearray(img.tobytes())
    # Init Transfer parameters
    f.write(b"P0\n# Packed\n")
    tempstr = str(w) + " " + str(h) + "\n" + "255\n"
    f.write(tempstr.encode())

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
                        if rotationAngle == 3:
                            buff_r[ii_] = Image_Data[i + 2]
                            buff_g[ii_] = Image_Data[i + 1]
                            buff_b[ii_] = Image_Data[i + 0]
                            buff_w[ii_] = round(((((buff_r[ii_] & 0xFF) >> 4) +
                                                  ((buff_g[ii_] & 0xFF) >> 4) +
                                                  ((buff_b[ii_] & 0xFF) >> 4)) / 3))
                        i += 8

                    for ii_ in range(round(w / 2)):
                        DataPack.append(((buff_r[ii_] & 0xF0) | ((buff_b[ii_] & 0xF0) >> 4)))

                    for ii_ in range(round(w / 2)):
                        DataPack.append(((((buff_w[ii_]) & 0x0F) << 4) | ((buff_g[ii_] & 0xF0) >> 4)))
                        # DataPack.append((((buff_w[ii_]) & 0x0F) << 4) | ((buff_g[ii_] & 0xF0) >> 4))


        #else: Unpacked работает для .pgm формата я его не добавлял
        #if i % w == 0:
            # SendData(DataPack)
            # DataPack.clear()
    print(binPath)
    f.write(bytearray(DataPack))
    f.close()

p = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
path = list()
for root, dirs, files in os.walk(p):
    for filename in files:
        if filename[-3:] == "png":
            path.append(p + filename)
print(path[0])
img = Image.open(path[0])
width, height = img.size

xCoord = 0
yCoord = 0
rotationAngle = 0   # 0-0 1-90 2-180 3-270
wave = 2            # 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
black = 0           # Черная корректировка значения: 0-15 в коде не использую если надо то можно добавить
white = 0           # Белая корректировка значения: 0-15 в коде не использую если надо то можно добавить
Partial = False
Packed = True

Repack(path[0], 0, 0, rotationAngle, wave, black, white, Partial, Packed)