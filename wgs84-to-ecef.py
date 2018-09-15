#!/usr/bin/env python3

# convert a lat/long/altitude to a 3D coordinate, or more specifically,
# convert WGS84 to ECEF

from math import *

# some constants
semi_major_axis = 6378137
semi_minor_axis = 6356752.314245
aa = semi_major_axis * semi_major_axis
ee = 1.0 - semi_minor_axis**2 / semi_major_axis**2  # first eccentricy squared


def prime_vertical_radius_of_curvature(latitude_radians):
    return semi_major_axis / sqrt(1.0 - ee * sin(latitude_radians))


def wgs84_to_ecef(latitude_degrees, longitude_degrees, height_meters):
    latitude_radians = radians(latitude_degrees)
    longitude_radians = radians(longitude_degrees)
    N = prime_vertical_radius_of_curvature(latitude_radians)

    return (
        (N + height_meters) * cos(latitude_radians) * cos(longitude_radians),
        (N + height_meters) * cos(latitude_radians) * sin(longitude_radians),
        ((1 - ee) * N + height_meters) * sin(latitude_radians)
    )

if __name__ == "__main__":
    meters_per_foot = 0.3048

    cda_lat = 47.6776800
    cda_long = -116.7804700
    cda_height = 2191 * meters_per_foot

    p1 = wgs84_to_ecef(cda_lat, cda_long, cda_height)
    p2 = wgs84_to_ecef(cda_lat, cda_long, cda_height + 1)

    from operator import sub
    normal = tuple(map(sub, p2, p1))
    length = sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)

    # I need one vector on plane
    # then that vector * normal will give another
    # vectors on plane are orthogonal

    print("p1 =", p1)
    print("p2 =", p2)
    print("normal =", normal)
    print("length =", length)
