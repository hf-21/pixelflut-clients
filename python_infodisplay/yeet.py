import os
import sys
import random
import time

from telnetlib import Telnet

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_utils.colors import rgb_dec_to_hex
from python_utils.text import get_text


HOST = os.getenv('PIXELFLUT_HOST')
PORT = os.getenv('PIXELFLUT_PORT')

WIDTH = 1920
HEIGHT = 1019

FG_COLOR = rgb_dec_to_hex(255, 255, 255)


def draw_text(tn):
    host_text = f"IP   : {HOST}"
    port_text = f"Port : {PORT}"

    x_offset = WIDTH-320
    y_offset = HEIGHT-40

    while True:

        host_fg_pixels, _ = get_text(host_text, 15)
        port_fg_pixels, _ = get_text(port_text, 15)

        for x, y in host_fg_pixels:
            tn.write(f'PX {x+x_offset} {y+y_offset} {FG_COLOR}\n'.encode())
        for x, y in port_fg_pixels:
            tn.write(f'PX {x+x_offset} {y+y_offset+20} {FG_COLOR}\n'.encode())


if __name__ == '__main__':
    with Telnet(HOST, PORT) as tn:
        draw_text(tn)
