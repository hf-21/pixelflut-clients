from math import radians, sin, cos


def circle(center_coord, radius=10):
    """Try to draw a circle"""

    vert = []

    # should be okay for smaller ones i guess
    points = radius * 7

    for i in range(points):
        angle = radians(float(i) / points * 360.0)
        x = radius * cos(angle) + center_coord[0]
        y = radius * sin(angle) + center_coord[1]
        vert.append((int(x), int(y)))

    return vert
