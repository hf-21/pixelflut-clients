import os
import sys
import random
import time

from telnetlib import Telnet

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_utils.colors import get_random_rgb
from python_utils.shapes import circle


HOST = os.getenv('PIXELFLUT_HOST')
PORT = os.getenv('PIXELFLUT_PORT')

WIDTH = 1920
HEIGHT = 1080

RADIUS = 100


def draw_circles(tn):

    cx = RADIUS
    cy = RADIUS

    color = get_random_rgb()

    gx = 5
    gy = 5
    while True:
        time.sleep(0.01)
        cx += gx
        cy += gy

        if cx+RADIUS > WIDTH or cx < 0+RADIUS:
            gx *= -1
            color = get_random_rgb()
        if cy+RADIUS > HEIGHT or cy < 0+RADIUS:
            gy *= -1
            color = get_random_rgb()

        c = circle((cx, cy), radius=RADIUS)

        for x, y in c:
            if x < 0 or y < 0:
                continue

            tn.write(f'PX {x} {y} {color}\n'.encode())


if __name__ == '__main__':
    with Telnet(HOST, PORT) as tn:
        draw_circles(tn)
