from math import sin, cos, sqrt

# major/minor axes in meters
SEMI_MAJOR_AXIS = 6_378_137
SEMI_MINOR_AXIS = 6_356_752.314_245

# first eccentricity squared
EE = 1.0 - SEMI_MINOR_AXIS**2 / SEMI_MAJOR_AXIS**2


def prime_vertical_radius_of_curvature(latitude_radians):
    sin_lat = sin(latitude_radians)

    return SEMI_MAJOR_AXIS / sqrt(1.0 - EE * sin_lat**2)


def wgs84_to_ecef(wgs84):
    (latitude_radians, longitude_radians, height_meters) = wgs84
    N = prime_vertical_radius_of_curvature(latitude_radians)

    return (
        (N + height_meters) * cos(latitude_radians) * cos(longitude_radians),
        (N + height_meters) * cos(latitude_radians) * sin(longitude_radians),
        ((1.0 - EE) * N + height_meters) * sin(latitude_radians)
    )
