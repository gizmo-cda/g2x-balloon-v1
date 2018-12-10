#!/usr/bin/env python3

import numpy as np
from math import degrees, radians
from utils.gps import wgs84_to_ecef
from utils.affine import *


def meters(feet):
    return feet * 0.304_800


if __name__ == "__main__":
    # np.set_printoptions(precision=3)

    # lat degrees long degrees, height feet
    cda = (
        radians(47.677_680_000),
        radians(-116.780_470_000),
        meters(2_191)
    )
    balloon = (
        radians(48),
        radians(-116.780_470_000),
        meters(100_000)
    )

    p1 = wgs84_to_ecef(cda)
    p2 = wgs84_to_ecef(balloon)

    print("cda = ", cda)
    print("balloon = ", balloon)
    print("p1 =", p1)
    print("p2 =", p2)

    t = translate(-p1[0], -p1[1], -p1[2])
    r1 = rotate_y(-cda[0])
    r2 = rotate_z(-cda[1])
    m = t @ r2 @ r1

    print(m)

    np_cda = np.array([p1[0], p1[1], p1[2], 1])
    np_balloon = np.array([p2[0], p2[1], p2[2], 1])

    print("cda 2 =", np.dot(np_cda, m))
    print("balloon 2 =", np.dot(np_balloon, m))
    print("declination =", degrees(angle_between(
        np.array([np_balloon[0], np_balloon[2]]),
        np.array([0, 1])
    )))
    print("right ascension =", degrees(angle_between(
        np.array([np_balloon[1], np_balloon[2]]),
        np.array([1, 0])
    )))
