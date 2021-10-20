from PIL import Image
from python_connector.connector import rgb_to_hex, Connector


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

    def frame_to_pixel(self, frame):
        y, x = frame.size
        row = 0
        pixel_data = []
        while row <= y - 1:
            column = 0
            while column <= x - 1:
                rgb = frame.convert('RGB').getpixel((row, column))
                hex_code = rgb_to_hex(rgb)
                pixel_data.append((row, column, hex_code))
                #data = data + "PX {x} {y} {hex}\n".format(x=row, y=column, hex=hex_code)
                column = column + 1
            row = row + 1
        return pixel_data
