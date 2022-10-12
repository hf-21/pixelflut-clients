import socket
host = ""
port = 8080
width = 1920
height = 1080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def value_tostring(x, y, value):
    request = ""
    for j in range(x):
        for i in range(y):
            request += "PX {0} {1} {2}{3}{4}\n".format(j , i , format(value, '02x'), format(value, '02x'), format(value, '02x'))

    return request

black = bytes(value_tostring(width, height, 255),'ascii')
white = bytes(value_tostring(width, height, 0), 'ascii')

while True:
    s.send(black)
    s.send(white)
