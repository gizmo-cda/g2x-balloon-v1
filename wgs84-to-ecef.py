#!/usr/bin/env python3

# convert a lat/long/altitude to a 3D coordinate, or more specifically,
# convert WGS84 to ECEF

from math import *
from operator import add, mul, sub

# major/minor axes in meters
semi_major_axis = 6_378_137
semi_minor_axis = 6_356_752.314_245

# first eccentricy squared
ee = 1.0 - semi_minor_axis**2 / semi_major_axis**2


def prime_vertical_radius_of_curvature(latitude_radians):
    sin_lat = sin(latitude_radians)

    return semi_major_axis / sqrt(1.0 - ee * sin_lat**2)


def wgs84_to_ecef(wgs84):
    (latitude_radians, longitude_radians, height_meters) = wgs84
    N = prime_vertical_radius_of_curvature(latitude_radians)

    return (
        (N + height_meters) * cos(latitude_radians) * cos(longitude_radians),
        (N + height_meters) * cos(latitude_radians) * sin(longitude_radians),
        ((1.0 - ee) * N + height_meters) * sin(latitude_radians)
    )


def wgs84_to_enu(from_wgs84, to_wgs84):
    from_ecef     = wgs84_to_ecef(from_wgs84)
    to_ecef       = wgs84_to_ecef(to_wgs84)
    vec           = (from_ecef[0] - to_ecef[0], from_ecef[1] - to_ecef[1], from_ecef[2] - to_ecef[2])
    (phi, lam, _) = to_wgs84

    print("from_wgs84 =", from_wgs84)
    print("to_wgs84 =", to_wgs84)
    print("from_ecef =", from_ecef)
    print("to_ecef =", to_ecef)
    print("vec =", vec)

    t0 = (
       -sin(lam),
        cos(lam),
        0
    )
    t1 = (
       -sin(phi) * cos(lam),
       -sin(phi) * sin(lam),
        cos(phi)
    )
    t2 = (
        cos(phi) * cos(lam),
        cos(phi) * sin(lam),
        sin(phi)
    )

    return (
        dot_product(t0, vec),
        dot_product(t1, vec),
        dot_product(t2, vec)
    )


def dot_product(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def meters(feet):
    return feet * 0.304_800


# Experimental functions

def point_on_surface(latitude_radians, longitude_radians):
    u = latitude_radians
    v = longitude_radians

    return (
        semi_major_axis * cos(u) * cos(v),
        semi_major_axis * cos(u) * sin(v),
        semi_minor_axis * sin(u)
    )


def normal_on_surface(latitude_radians, longitude_radians):
    p3 = point_on_surface(latitude_radians, longitude_radians)

    dx = 2 / (semi_major_axis * semi_major_axis)
    dy = dx
    dz = 2 / (semi_minor_axis * semi_minor_axis)

    p4 = (
        p3[0] * dx,
        p3[1] * dy,
        p3[2] * dz
    )

    length = sqrt(p4[0]**2 + p4[1]**2 + p4[2]**2)
    
    return (
        p4[0] / length,
        p4[1] / length,
        p4[2] / length
    )


if __name__ == "__main__":
    # lat, long, height
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
    v1 = wgs84_to_enu(cda, balloon)

    print("height =", cda[2])
    print("p1 =", p1)
    print("p2 =", p2)
    print("v1 =", v1)
    print()
