import os

from PIL import Image, ImageFont, ImageDraw

from typing import Tuple, List

FONTFILE =  os.getenv('PIXELFLUT_FONT')


def get_text(text: str, size: int = 10) -> Tuple[List[int], List[int]]:
    """Return pixels for the given text with the given size"""

    assert FONTFILE and os.path.isfile(FONTFILE), f'Font file "{FONTFILE}" not found!'

    font = ImageFont.truetype(FONTFILE, size)
    size = font.getsize(text)
    image = Image.new('1', size, 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)

    fg_pixels = []
    bg_pixels = []

    for x in range(size[0]):
        line = []
        for y in range(size[1]):
            if image.getpixel((x, y)):
                bg_pixels.append((x, y))
            else:
                fg_pixels.append((x, y))

    return fg_pixels, bg_pixels
