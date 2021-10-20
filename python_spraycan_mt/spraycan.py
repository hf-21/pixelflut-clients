import multiprocessing
import socket
import numpy as np
import multiprocessing as mp
import threading as tp
host = ""
port = 8080


def send_patch(x_offset, y_offset):
    global host
    global port
    x = 100
    y = 100
    r = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    b = np.random.randint(0, 255)
    request = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    for j in range(x):
        for i in range(y):
            request += "PX {0} {1} {2}{3}{4}\n".format(i + x_offset, j + y_offset, format(r, '02x'), format(g, '02x'),
                                                       format(b, '02x'))

    s.send(bytes(request, 'ascii'))


def send_patch_random(size):
    global host
    global port
    x = size
    y = size
    x_offset = np.random.randint(0, 1920 - x)
    y_offset = np.random.randint(0, 1080 - y)
    r = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    b = np.random.randint(0, 255)
    request = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    for j in range(x):
        for i in range(y):
            request += "PX {0} {1} {2}{3}{4}\n".format(i + x_offset, j + y_offset, format(r, '02x'), format(g, '02x'), format(b, '02x'))

    s.send(bytes(request, 'ascii'))


def spraycan_multiprocessing(square_size):
    with mp.Pool(processes=16) as pool:
        pool.map(send_patch_random, [square_size]*1000000)


if __name__ == '__main__':
    spraycan_multiprocessing(100)
