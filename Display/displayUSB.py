from PIL import Image
import serial.tools.list_ports
import serial
import time
import sys

class DisplayUSB:

    _port = serial.Serial()

    def connect(self):
        '''
        Подключиться через com порт
        '''
        ports = list(serial.tools.list_ports.comports())  # Получаем порты
        portName = str(ports[0]).split(" ")[0]  # Берем из полученного только название
        try:
            if (self._port.is_open):
                self._port.setRTS(False)
                self._port.setDTR(False)
                self._port.close()
                time.sleep(250)
            self._port.baudrate = 9600
            self._port.port = portName
            self._port.setRTS(True)
            self._port.setDTR(True)
            self._port.timeout = None
            self._port.parity = serial.PARITY_SPACE
            self._port.open()
            print(self._port)

        except Exception:
            print("Ошибка открытия СОМ порта\n")
            sys.exit()

    def sendData(self, data):
        if data == None:
            print("Data is none")
            return
        if len(data) < 1:
            print("No data")
            return
        if self._port == None:
            print("Port is none")
            return
        if self._port.is_open == False:
            print("Port is close")
            return
        values = bytearray(data)
        self._port.write(values)

    def clearScreen(self, colorUpDown):
        '''
        :param colorUpDown: каким цветом закрасить: 0-черный, 15 - белый
        '''
        DataPack = list()
        DataPack.append(0x88)
        DataPack.append(0x32)
        DataPack.append(0x03)
        DataPack.append(colorUpDown)
        DataPack.append(0x00)
        DataPack.append(0x00)
        self.sendData(DataPack)

    def load(self, path):
        '''
        Вывести изображение на экран
        :param path: путь к изображению закодированному в bin
        '''
        DataPack = list()
        with open(path, 'rb') as bin:
            i = 0
            while i < 12:
                current_byte = bin.read(1)
                if (not current_byte):
                    break
                DataPack.append(ord(current_byte))
                i += 1
            self.sendData(DataPack)
            DataPack.clear()
            while True:
                current_byte = bin.read(1)
                if (not current_byte):
                    break
                DataPack.append(ord(current_byte))
            self.sendData(DataPack)
            DataPack.clear()
            DataPack.append(0x00)
            DataPack.append(0x00)
            self.sendData(DataPack)
            DataPack.clear()
            self._port.close()

    def repack(self, path, xCoord, yCoord, rotationAngle, wave, black, white, Partial, Packed):
        '''
        Конвертирует из png в bin
        сохраняет в директорию в которой оригинал
        :param path: путь к изображению
        :param xCoord:
        :param yCoord:
        :param rotationAngle: 0-0 1-90 2-180 3-270
        :param wave: 0 - 3 bit 0 - init_clear 1 - refresh 2 - delta 3 - refresh_mono 4 - delta_mono
        :param black: Черная корректировка значения: 0-15
        :param white:  Белая корректировка значения: 0-15
        :param Partial:
        :param Packed:
        '''
        DataPack = list()
        Image_Data = list()

        typeOfFile = path[-4:]
        binPath = path[0: -3] + "bin"
        print(path)

        f = open(binPath, "wb")

        w = 0
        h = 0
        if typeOfFile == ".png":
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

        f.write(bytearray(DataPack))
        DataPack.clear()
        offset = 1
        if typeOfFile == ".png":
            offset = w * 7
        buff_r = [None] * w
        buff_g = [None] * w
        buff_b = [None] * w
        buff_w = [None] * w

        i = 0
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
        print(binPath)
        f.write(bytearray(DataPack))
        f.close()
