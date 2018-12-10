#!/usr/bin/env python3

import numpy as np
from math import cos, sin, degrees, radians, sqrt
from utils.gps import wgs84_to_ecef, SEMI_MAJOR_AXIS
from utils.affine import *

def rotate_target(declination, ascension, radius):
    x = radius * sin(ascension) * cos(declination)
    y = radius * sin(ascension) * sin(declination)
    z = radius * cos(ascension)

    return np.array([x, y, z, 1])

    # rot_x = rotate_x(declination)
    # rot_z = rotate_z(-ascension)
    # rotation_matrix = rot_x @ rot_z
    # vector = np.array([0, radius, 0, 1])

    # return np.dot(vector, rotation_matrix)


if __name__ == "__main__":
    latitude = radians(0)
    longitude = radians(0)
    altitude = 0

    rot_y = rotate_y(-latitude)
    rot_z = rotate_z(-longitude)
    rotation_matrix = rot_y @ rot_z

    radius = 100
    target_declination = radians(45)
    target_ascension = radians(0)

    origin = np.array([SEMI_MAJOR_AXIS, 0, 0, 1])
    target_vector = rotate_target(target_declination, target_ascension, radius)
    target = np.array([
        origin[0] + target_vector[0],
        origin[1] + target_vector[1],
        origin[2] + target_vector[2],
        1
    ])

    print("target_vector =", target_vector)
    print("length =", np.linalg.norm(target_vector))

    # print(origin)
    # print(target)

    new_origin = np.dot(origin, rotation_matrix)
    new_target = np.dot(target, rotation_matrix)
    vector = np.array([
        new_target[0] - new_origin[0],
        new_target[1] - new_origin[1],
        new_target[2] - new_origin[2]
    ])

    # print(new_origin)
    # print(new_target)
    # print(vector)

    u_vector = np.array([0, 1])
    uv_vector = np.array([
        vector[1],
        vector[2]
    ])
    vw_vector = np.array([
        vector[0],
        vector[2]
    ])

    # print(uv_vector)
    # print(vw_vector)

    declination = degrees(angle_between(uv_vector, u_vector))
    ascension = degrees(angle_between(vw_vector, u_vector))

    print("target declination =", degrees(target_declination))
    print("target ascension   =", degrees(target_ascension))
    print("declination        =", declination)
    print("ascension          =", ascension)
