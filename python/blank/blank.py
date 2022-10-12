"""Empty the canvas once"""

import os
import time

from telnetlib import Telnet


HOST = os.getenv('PIXELFLUT_HOST')
PORT = os.getenv('PIXELFLUT_PORT')

HEIGHT = 1080
WIDTH = 1920

COLOR = '111111'


def draw_blank(tn):
    while True:
        line = str()
        for x in range(0, WIDTH):
            for y in range(0, HEIGHT):
                line += f'PX {x} {y} {COLOR}\n'
        tn.write(line.encode())
        time.sleep(10)


if __name__ == '__main__':
    with Telnet(HOST, PORT) as tn:
        draw_blank(tn)
