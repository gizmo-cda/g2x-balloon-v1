#!/usr/bin/env python3

import csv
from math import sin, cos, sqrt, radians
import time


# major/minor axes in meters
semi_major_axis = 6_378_137
semi_minor_axis = 6_356_752.314_245

# first eccentricity squared
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


with open('gps_20180529.csv', 'r') as f:
    reader = csv.reader(f)

    header = next(reader)
    print(",".join(["epoch_time", "time", "dt", "dist", "vel", "accel"]))
    last_x = None
    last_y = None
    last_z = None
    last_time = None
    last_vel = None

    for row in reader:
        epoch_time = time.mktime(time.strptime("{} {}".format(row[0], row[1]), "%m/%d/%y %H:%M:%S"))

        if epoch_time > 1527657834:
            break

        (x, y, z) = wgs84_to_ecef((
            radians(float(row[2])),
            radians(float(row[3])),
            float(row[6])
        ))

        if last_x != x or last_y != y or last_z != z:
            if last_x is not None:
                dx = x - last_x
                dy = y - last_y
                dz = z - last_z
                dt = epoch_time - last_time
                dist = sqrt(dx*dx + dy*dy + dz*dz)
                vel = dist/dt

                if last_vel is not None:
                    accel = (vel - last_vel) / dt
                else:
                    accel = 0
            else:
                dist = 0
                vel = 0
                accel = 0
                dt = 0

            print(",".join([str(epoch_time), str(row[1]), str(dt), str(dist), str(vel), str(accel)]))

            last_x = x
            last_y = y
            last_z = z
            last_time = epoch_time
            last_vel = vel
