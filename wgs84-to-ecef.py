#!/usr/bin/env python3

# convert a lat/long/altitude to a 3D coordinate, or more specifically,
# convert WGS84 to ECEF

from math import *

# major/minor axes in meters
semi_major_axis = 6_378_137
semi_minor_axis = 6_356_752.314_245

# first eccentricy squared
ee = 1.0 - semi_minor_axis**2 / semi_major_axis**2


def prime_vertical_radius_of_curvature(latitude_radians):
    sin_lat = sin(latitude_radians)

    return semi_major_axis / sqrt(1.0 - ee * sin_lat**2)


def wgs84_to_ecef(latitude_degrees, longitude_degrees, height_meters):
    latitude_radians = radians(latitude_degrees)
    longitude_radians = radians(longitude_degrees)
    N = prime_vertical_radius_of_curvature(latitude_radians)

    return (
        (N + height_meters) * cos(latitude_radians) * cos(longitude_radians),
        (N + height_meters) * cos(latitude_radians) * sin(longitude_radians),
        ((1.0 - ee) * N + height_meters) * sin(latitude_radians)
    )


if __name__ == "__main__":
    from operator import sub

    meters_per_foot = 0.304_800

    for height in (0.0, 2191.0, 100_000.0):
        cda_lat = 47.677_680_000
        cda_long = -116.780_470_000
        cda_height = height * meters_per_foot

        p1 = wgs84_to_ecef(cda_lat, cda_long, cda_height)
        p2 = wgs84_to_ecef(cda_lat, cda_long, cda_height + 1.0)

        normal = tuple(map(sub, p2, p1))
        length = sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)

        # I need one vector on plane
        # then that vector cross normal will give another vector
        # these vectors on plane will be orthogonal

        print("height =", cda_height)
        print("p1 =", p1)
        print("p2 =", p2)
        print("normal =", normal)
        print("length =", length)
        print()
