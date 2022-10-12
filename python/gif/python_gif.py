from PIL import Image
from python_utils.colors import rgb_dec_to_hex
from os.path import exists
import pickle


class Gif:
    """
    Fetch a gif
    curl https://media.giphy.com/media/lgcUUCXgC8mEo/giphy.gif --output ~/path/rickroll.gif
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def get_size(self):
        image_object = Image.open(self.file_path)
        return image_object.size

    def get_frames(self):
        image_object = Image.open(self.file_path)
        for frame_number in range(0, image_object.n_frames):
            image_object = Image.open(self.file_path)
            image_object.seek(frame_number)
            print("Frame number: {}".format(frame_number))
            yield image_object

    def _frame_to_pixel(self, frame):
        y, x = frame.size
        row = 0
        pixel_data = []
        while row <= y - 1:
            column = 0
            while column <= x - 1:
                r, g, b = frame.convert('RGB').getpixel((row, column))
                hex_code = rgb_dec_to_hex(r, g, b)
                pixel_data.append((row, column, hex_code))
                #data = data + "PX {x} {y} {hex}\n".format(x=row, y=column, hex=hex_code)
                column = column + 1
            row = row + 1
        return pixel_data

    def get_frames_as_pixel_set(self, start_x=None, start_y=None):
        gif_name = self.file_path.split('.')[0]
        pickle_file = gif_name + '.pkl'
        if not exists(pickle_file):
            frames = []
            for frame in self.get_frames():
                frames.append(self._frame_to_pixel(frame))
            with open(gif_name + '.pkl', 'wb') as f:
                pickle.dump(frames, f)
        else:
            with open(pickle_file, 'rb') as f:
                frames = pickle.load(f)

        if start_x and start_y:
            offset_frames = []
            for frame in frames:
                offset_frames.append(self.set_offset(start_x, start_y, frame))

            frames = offset_frames

        return frames

    def set_offset(self, start_x, start_y, frame):
        offset_frame = []
        for x, y, color in frame:
            offset_frame.append((x + start_x, y + start_y, color))
        return offset_frame

