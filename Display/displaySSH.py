from PIL import Image
import paramiko
import os
from invoke import Responder
from fabric import Connection

class DisplaySSH:
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
        :return:
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

    def sendSSH(self, fromPath, toPath, host, user, pwd, port):
        '''
        Отправляет по SSH все содержимое директории fromPath на хост в toPath
        :param fromPath:
        :param toPath:
        :param host:
        :param user:
        :param pwd: пароль
        :param port:
        :return:
        '''

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=pwd, port=port)
        print(host)

        sftp = client.open_sftp()
        for root, dirs, files in os.walk(fromPath):
            for filename in files:
                sftp.put(fromPath + filename, toPath + filename)
                print("send",fromPath + filename)
        client.close()

    def ranScriptSSH(self, script, host, user, pwd, port):
        '''
        Запускает скрипт на хосте
        :param host:
        :param user:
        :param pwd: пароль
        :param port:
        :return:
        '''
        cmd = 'sudo python2 ' + script
        c = Connection(host=host, user=user, connect_kwargs={"password": pwd}, port=port)
        sudopass = Responder(pattern=r'\[sudo\] password:', response='temppwd\n', )
        # c.sudo('sudo python3 /var/lib/cloud9/Projects/ver_0.2/loader.py', pty=True, watchers=[sudopass])
        # c.sudo('sudo python2 /var/lib/cloud9/Projects/ver_0.2/main.py', pty=True, watchers=[sudopass])
        c.sudo(cmd, pty=True, watchers=[sudopass])

