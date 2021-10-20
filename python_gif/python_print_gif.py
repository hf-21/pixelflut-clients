import pickle

from python_gif import Gif
from time import sleep
from python_connector.connector import Connector
from os.path import isfile


def yeet_the_gif(gif_path, start_x=None, start_y=None):
    gif_name = gif_path.split('.')[0]
    pickle_file = gif_name + '.pkl'
    if not isfile(pickle_file):
        gif = Gif(gif_path)

        frames = []
        for frame in gif.get_frames():
            frames.append(gif.frame_to_pixel(frame))
        with open(gif_name + '.pkl', 'rb') as f:
            pickle.dump(frames, f)
    else:
        with open(pickle_file, 'rb') as f:
            frames = pickle.load(f)

    if start_x and start_y:
        offset_frames = []
        for frame in frames:
            offset_frames.append(set_offset(start_x, start_y, frame))

        frames = offset_frames

    frames_numbers = len(frames)
    n = 0

    with Connector() as c:
        while True:
            if n == frames_numbers:
                n = 0
            sleep(0.05)
            c.set_pixel_bulk(frames[n])
            n = n + 1


def set_offset(start_x, start_y, frame):
    offset_frame = []
    for x, y, color in frame:
        offset_frame.append((x + start_x, y + start_y, color))
    return offset_frame
