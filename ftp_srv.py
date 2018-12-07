from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

authorizer = DummyAuthorizer()
authorizer.add_user('user', '12345', '.', perm='elradfmw')
authorizer.add_anonymous('.')

handler = FTPHandler
handler.authorizer = authorizer

# Instantiate FTP server class and listen on 0.0.0.0:2121
address = ('', 2121)
server = FTPServer(address, handler)

handler.banner = "pyftpdlib based ftpd ready."
# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5

# start ftp server
server.serve_forever()