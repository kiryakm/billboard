import paramiko
import os
from invoke import Responder
from fabric import Connection

def sendSSH(host, user, pwd, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=pwd, port=port)
    print(host)

    FromPath = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
    ToPath = "/var/lib/cloud9/Projects/ver_0.2/ImageForPrint/"

    sftp = client.open_sftp()
    for root, dirs, files in os.walk(FromPath):
        for filename in files:
            sftp.put(FromPath + filename, ToPath + filename)
            print(FromPath + filename)
    client.close()


def ranScriptSSH(host, user, pwd, port):
    c = Connection(host=host, user=user,connect_kwargs={"password": pwd},  port=port)
    sudopass = Responder(pattern=r'\[sudo\] password:',response='temppwd\n',)
    #c.sudo('sudo python3 /var/lib/cloud9/Projects/ver_0.2/loader.py', pty=True, watchers=[sudopass])
    c.sudo('sudo python2 /var/lib/cloud9/Projects/ver_0.2/main.py', pty=True, watchers=[sudopass])


host = '192.168.8.1'
user = 'debian'
pwd = 'temppwd'
port = 22


