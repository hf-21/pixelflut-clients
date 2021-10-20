import os
import sys
import random
import time

from telnetlib import Telnet

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_utils.colors import get_random_rgb
from python_utils.text import get_text


HOST = os.getenv('PIXELFLUT_HOST')
PORT = os.getenv('PIXELFLUT_PORT')

WIDTH = 1920
HEIGHT = 1019


def draw_text(tn):
    host_text = f"IP   : {HOST}"
    port_text = f"Port : {PORT}"

    x_offset = WIDTH-320
    y_offset = HEIGHT-40

    i = 0
    color = get_random_rgb()
    while True:
        i = i + 1

        if not i % 100:
            i = 0
            color = get_random_rgb()

        host_fg_pixels, _ = get_text(host_text, 15)
        port_fg_pixels, _ = get_text(port_text, 15)

        for x, y in host_fg_pixels:
            tn.write(f'PX {x+x_offset} {y+y_offset} {color}\n'.encode())
        for x, y in port_fg_pixels:
            tn.write(f'PX {x+x_offset} {y+y_offset+20} {color}\n'.encode())


if __name__ == '__main__':
    with Telnet(HOST, PORT) as tn:
        draw_text(tn)
