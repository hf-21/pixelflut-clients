import cv2
import os
import threading
from telnetlib import Telnet

HOST = os.getenv('PIXELFLUT_HOST')
PORT = os.getenv('PIXELFLUT_PORT')


def webcam_fun():
    cam = cv2.VideoCapture(0)


    while True:
        ret_val, img = cam.read()
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        gen_pixel(img)



def gen_pixel(img):
    rows, cols, _ = img.shape
    frame_string = ""
    x_offset = 950
    y_offset = 350

    for y in range(0, cols, 3):
        for x in range(0, rows, 3):
            b, g, r = img[x][y]

            string_stuff = ("PX {0} {1} {2}{3}{4}10\n".format(x + x_offset, y + y_offset, format(r, '02x'), format(g, '02x'),
                                                format(b, '02x')))
            frame_string = frame_string + string_stuff
    with Telnet(HOST, PORT) as tn:
        tn.write(frame_string.encode())



def draw_blank():
    x_offset = 950
    y_offset = 350
    frame_string=""
    for y in range(0, 480):
        for x in range(0, 640, 3):
            string_stuff = ("PX {0} {1} {2}{3}{4}\n".format(x + x_offset, y + y_offset, format(00, '02x'), format(00, '02x'),
                                                    format(00, '02x')))
            frame_string = frame_string + string_stuff
    with Telnet(HOST, PORT) as tn:
        tn.write(frame_string.encode())



if __name__ == '__main__':
    webcam_fun()
