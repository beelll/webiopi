import socket
from contextlib import closing
import sys

s = socket.socket()

host = '192.168.0.18'
port = 5000

#with closing(s):
s.connect((host, port))
s.send("getTemperature")
#while True:
print s.recv(4096)

