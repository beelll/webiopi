import socket
from contextlib import closing
import sys

def getTemp():
    s = socket.socket()

    host = '192.168.0.18'
    port = 5000

    #with closing(s):
    s.connect((host, port))
    s.send("getTemperature")
    #while True:
    ret = s.recv(4096)
    return ret


# Call getTemperature() only when it is executed directry
if __name__ == '__main__':
    getTemp()


