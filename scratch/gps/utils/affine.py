import numpy as np
from math import cos, sin


def identity():
    return np.identity(4);

def translate(x, y, z):
    return np.array((
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (x, y, z, 1)
    ))

def rotate_x(angle):
    c = cos(angle)
    s = sin(angle)

    return np.array((
        (1,  0, 0, 0),
        (0,  c, s, 0),
        (0, -s, c, 0),
        (0,  0, 0, 1)
    ))

def rotate_y(angle):
    c = cos(angle)
    s = sin(angle)

    return np.array((
        (c, 0, -s, 0),
        (0, 1,  0, 0),
        (s, 0,  c, 0),
        (0, 0,  0, 1)
    ))

def rotate_z(angle):
    c = cos(angle)
    s = sin(angle)

    return np.array((
        ( c, s, 0, 0),
        (-s, c, 0, 0),
        ( 0, 0, 1, 0),
        ( 0, 0, 0, 1)
    ))

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)

    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
