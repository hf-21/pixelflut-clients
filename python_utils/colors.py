import random


def rgb_dec_to_hex(r: int, g: int, b: int) -> str:
    """Return int values (0-255) to rgb hex codes"""

    assert 0 <= r < 256, "r value must be between 0 and 255"
    assert 0 <= g < 256, "g value must be between 0 and 255"
    assert 0 <= b < 256, "b value must be between 0 and 255"

    return f'{r:02X}{g:02X}{b:02X}'


def get_random_rgb() -> str:
    """Generate random RGB value"""

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return rgb_dec_to_hex(r, g, b)
