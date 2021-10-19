import random


def get_random_rgb():
    """Generate random RGB value"""

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return f'{r:02X}{g:02X}{b:02X}'
