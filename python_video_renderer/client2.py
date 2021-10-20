import socket
import numpy as np
import cv2
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
import time
import itertools

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 8080
s.connect((host, port))
send = s.send


def video_to_array(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    buffer = np.empty((frame_count, frame_height, frame_width, 3), np.dtype('uint8'))
    fc = 0
    ret = True
    while (fc < frame_count and ret):
        ret, buffer[fc] = cap.read()
        fc += 1
    cap.release()
    return buffer


def send_rendered_frame(rendered_frame):
    global host
    global port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sock.send(bytes(rendered_frame, 'ascii'))


def send_chunk(chunk):
    global host
    global port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(bytes("".join(chunk), 'ascii'))


def send_rendered_frame_multiprocess(rendered_frame):
    with mp.Pool(processes=16) as pool:
        pool.map(send_chunk, rendered_frame)


def render_frame(frame, h, y_offset, x_offset):
    y, x, n = frame.shape
    rendered_chunk = []
    for j in range(y):
        for i in range(x):
            b, g, r = frame[j][i]
            rendered_chunk.append("PX {0} {1} {2}{3}{4}\n".format(i + x_offset, j + h + y_offset, format(r, '02x'), format(g, '02x'), format(b, '02x')))

    return rendered_chunk


def render_frame_multiprocess(frame, y_offset, x_offset):
    with mp.Pool(processes=16) as pool:
        y, x, n = frame.shape
        rows = []
        for row in range(int(y/16), y, int(y/16)):
            rows.append(frame[row-int(y/16):row])
        rows = np.array(rows)
        rendered = pool.starmap(render_frame, zip(rows, range(0, y, int(y/16)), [y_offset]*int(y/16), [x_offset]*int(y/16)))
        result = ""
        for i in range(16):
            result += "".join(rendered[i])
        return result


def send_video(video_path, x_offset=0, y_offset=0):
    buffer = video_to_array(video_path)

    frame_count, y, x, n = buffer.shape
    rendered_frames = []

    for frame in range(100, 150):
        print("frame rendered " + str(frame))
        rendered_frames.append(render_frame_multiprocess(buffer[frame], y_offset, x_offset))

    [send_rendered_frame(frame) for frame in rendered_frames]
    for i, frame in enumerate(rendered_frames):
        print("frame send " + str(i))

        send_rendered_frame(frame)

def spam_image_from_video(video_path, frame_number, x_offset=0, y_offset=0):
    buffer = video_to_array(video_path)
    to_send = render_frame_multiprocess(buffer[frame_number], y_offset, x_offset)
    while True:
        send_rendered_frame(to_send)

if __name__ == '__main__':
    # spam_image_from_video("beach.mp4", 60)
    send_video("beach.mp4")
