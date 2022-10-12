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
    text = [
        f"IP   : {HOST}",
        f"Port : {PORT}",
    ]

    line_spacing = 10
    line_height = 25

    _text = list()
    for line in text:
        _text.append(get_text(line, line_height))

    text_width = max(i[2] for i in _text)
    text_height = sum(i[3] for i in _text)

    x_offset = 25  #int(WIDTH / 2 - text_width / 2)
    y_offset = HEIGHT - text_height  #int(HEIGHT - text_height) - 50

    i = 0
    color = get_random_rgb()
    while True:
        time.sleep(0.01)
        i = i + 1

        if not i % 100:
            i = 0
            color = get_random_rgb()

        for _i, _line in enumerate(_text):
            y_line_offset = _i * (_line[3] + line_spacing)
            for x, y in _line[0]:
                tn.write(f'PX {x+x_offset} {y+y_offset+y_line_offset} {color}\n'.encode())



if __name__ == '__main__':
    with Telnet(HOST, PORT) as tn:
        draw_text(tn)
