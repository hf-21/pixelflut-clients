import numpy as np
import socket
from scipy.ndimage.filters import gaussian_filter


def calc_amount_bytes(x, y):
    n = 0
    for i in range(y):
        for j in range(x):
            n += 12 + len(str(i)) + len(str(j))
    return n


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.0.0.1"
port = 8080
s.connect((host, port))
sigma = 18

x = 500
y = 500
x_offset = 200
y_offset = 200

currently_displayed_r = np.full((x,y), 0)
currently_displayed_g = np.full((x,y), 0)
currently_displayed_b = np.full((x,y), 0)
currently_displayed_rgb = np.full((x,y,3), 0)
request = ""
for i in range(y_offset, y + y_offset):
    for j in range(x_offset, x + x_offset):
        request += f"PX {j} {i}\n"
s.send(bytes(request, 'ascii'))
data = recvall(s, calc_amount_bytes(x, y))
data = str(data, 'ascii')
data = data.split("\n")

for i, pixel in enumerate(data[:len(data)-1]):
    pixel = pixel.split(" ")
    #print(int(pixel[1]))
    lx = int(pixel[1])
    ly = int(pixel[2])
    pixel = pixel[-1]
    #print(i)
    color = pixel
    currently_displayed_r[ly - y_offset][lx - x_offset] = int(str("0x"+color[:2]), base=16)
    currently_displayed_g[ly - y_offset][lx - x_offset] = int(str("0x"+color[2:4]), base=16)
    currently_displayed_b[ly - y_offset][lx - x_offset] = int(str("0x"+color[4:6]), base=16)


guassian_r = gaussian_filter(currently_displayed_r, sigma=sigma, mode="mirror")
guassian_g = gaussian_filter(currently_displayed_g, sigma=sigma, mode="mirror")
guassian_b = gaussian_filter(currently_displayed_b, sigma=sigma, mode="mirror")
request = ""
print("halftime")
for i in range(y):
    for j in range(x):
        r,g,b = guassian_r[i][j], guassian_g[i][j], guassian_b[i][j]
        request += "PX {0} {1} {2}{3}{4}\n".format(j + x_offset, i + y_offset, format(r, '02x'), format(g, '02x'), format(b, '02x'))
s.send(bytes(request, 'ascii'))
