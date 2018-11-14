#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
general object to handle relative positioning

* note on surface normal: http://www.geo.hunter.cuny.edu/~jochen/GTECH201/Lectures/Lec6concepts/05%20-%20Understanding%20datums.html
* good article on wg84 history: https://frontierprecision.com/wp-content/uploads/EvolutionofWGS84andNAD83.pdf


* gps coordinates, guide to google maps verification: https://www.ubergizmo.com/how-to/read-gps-coordinates/

The simplest way to transform coordinates in Python is pyproj, i.e. the
Python interface to PROJ.4 library. https://gis.stackexchange.com/questions/78838/converting-projected-coordinates-to-lat-lon-using-python/78944#78944
"""
import typing as _typing
import math as _math
import numpy as _np
import math as math

class latlon(_typing.NamedTuple):
    deg: float
    minute: float
    second: float
    hemisphere: _typing.AnyStr

# http://spatialreference.org/ref/epsg/4326/
# WGS84 Bounds: -180.0000, -90.0000, 180.0000, 90.0000
class wgs84tup(_typing.NamedTuple):
    latitude_rad: float
    longitude_rad: float
    elevation_m: float

class xyz(_typing.NamedTuple):
    x: float
    y: float
    z: float

class out_look_at(_typing.NamedTuple):
    angle_rad_between_unit_vectors: float
    unit_vector_axis_of_rotation: xyz
    unit_vector_to_target: xyz

#-------ripped from gps\wgs84-to-ecef.py--------

# major/minor axes in meters
semi_major_axis = 6_378_137  # m
semi_minor_axis = 6_356_752.314_245  # m

# first eccentricy squared
ee = 1.0 - semi_minor_axis**2 / semi_major_axis**2


def prime_vertical_radius_of_curvature(latitude_radians):
    sin_lat = _math.sin(latitude_radians)
    return semi_major_axis / _math.sqrt(1.0 - ee * sin_lat**2)


def wgs84_to_ecef(wgs84: wgs84tup):
    N = prime_vertical_radius_of_curvature(wgs84.latitude_rad)

    return xyz(
        x=(N + wgs84.elevation_m) * _math.cos(wgs84.latitude_rad) * _math.cos(wgs84.longitude_rad),
        y=(N + wgs84.elevation_m) * _math.cos(wgs84.latitude_rad) * _math.sin(wgs84.longitude_rad),
        z=((1.0 - ee) * N + wgs84.elevation_m) * _math.sin(wgs84.latitude_rad),
    )
#-------ripped from gps\wgs84-to-ecef.py--------

def delta_xyz(curr_xyz, targ_xyz):
    delta_x = float(targ_xyz.x - curr_xyz.x)
    delta_y = float(targ_xyz.y - curr_xyz.y)
    delta_z = float(targ_xyz.z - curr_xyz.z)
    return xyz(x=delta_x, y=delta_y, z=delta_z)

def unit_vector_to_target(current_pos, target_pos):
    deltas = delta_xyz(curr_xyz=current_pos, targ_xyz=target_pos)
    print(f'deltas.x: {deltas.x:.5}')
    print(f'deltas.y: {deltas.y:.5}')
    print(f'deltas.z: {deltas.z:.5}')
    maxval = max(deltas)
    return xyz(x=deltas.x / maxval, y=deltas.y / maxval, z=deltas.z / maxval)

def dot_product(vect1, vect2):
    dot_sum = 0
    if len(vect1) != len(vect2) or len(vect1) == 0:
        raise IOError('something wrong')
    for (ax1, ax2) in zip(vect1, vect2):
        dot_sum += ax1 * ax2
    return dot_sum

def cross_product(A, B):
    """
    Both the two operands and the result of the cross product are vectors.
    The vector cross product has some useful properties, it produces a vector which is mutually perpendicular to the two vectors being multiplied.
    The vector cross product gives a vector which is perpendicular to both the vectors being multiplied. The resulting vector A × B is defined by:
    x = Ay * Bz - By * Az
    y = Az * Bx - Bz * Ax
    z = Ax * By - Bx * Ay
    where x,y and z are the components of A x B
    """
    x = A.y * B.z - B.y * A.z
    y = A.z * B.x - B.z * A.x
    z = A.x * B.y - B.x * A.y
    return xyz(x=x, y=y, z=z)

def look_at(current_pos, target_pos, current_view_unit=xyz(x=1, y=0, z=0)):
    ntarget = unit_vector_to_target(
        current_pos=current_pos, target_pos=target_pos, )
    dot_mag = dot_product(vect1=ntarget, vect2=current_view_unit)
    angle_rad_between_unit_vectors = _math.acos(dot_mag)
    print(f'rot-deg: {angle_rad_between_unit_vectors * 180 / _math.pi:.5}')

    rot_vector = cross_product(A=ntarget, B=current_view_unit)
    return out_look_at(
        angle_rad_between_unit_vectors=angle_rad_between_unit_vectors,
        unit_vector_axis_of_rotation=rot_vector,
        unit_vector_to_target=ntarget,
    )

def conv_deghms_2_radians(deg, minute, second, hemisphere):
    r"""
    gps annotations:
        ° : degree
        ' : minute
        " : second
    1 degree is equal to 1 hour, that is equal to 60 minutes or 3600 seconds.
    To calculate decimal degrees, we use the DMS to decimal degree formula below:
    Decimal Degrees = degrees + (minutes/60) + (seconds/3600)
    source: https://www.latlong.net/degrees-minutes-seconds-to-decimal-degrees

    hemisphere is relative to the prime meridian
    https://msdn.microsoft.com/en-us/library/aa578799.aspx
    """
    deg_all = deg + (minute / 60.) + (second / 3600.)
    rad_all = _math.radians(deg_all)
    if hemisphere.lower() in ('S', 'W'):
        rad_all *= -1
    return rad_all

# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta):
    r"""
    https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    """
     
    R_x = _np.array([[1,         0,                  0                   ],
                     [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                     [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                     ])
         
         
                     
    R_y = _np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                     [0,                     1,      0                   ],
                     [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                     ])
                 
    R_z = _np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                     [math.sin(theta[2]),    math.cos(theta[2]),     0],
                     [0,                     0,                      1]
                     ])
                     
                     
    R = _np.dot(R_z, _np.dot( R_y, R_x ))
 
    return R  # Rotation Matrix

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = _np.transpose(R)
    shouldBeIdentity = _np.dot(Rt, R)
    I = _np.identity(3, dtype = R.dtype)
    n = _np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6
 
 
# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
 
    assert(isRotationMatrix(R))
     
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return _np.array([x, y, z])

def gps_loc_plane_unit_vectors(gps_location: wgs84tup):
    rotation_matrix = eulerAnglesToRotationMatrix(theta=[
        0,
        gps_location.latitude_rad,  # latitude rotation about y
        gps_location.longitude_rad,  # longitude rotation about z
    ])
    # unit_look_vectors
    plane_x_unit_abs = rotation_matrix @ _np.array(xyz(x=1, y=0, z=0))
    plane_y_unit_abs = rotation_matrix @ _np.array(xyz(x=0, y=1, z=0))
    plane_z_unit_abs = rotation_matrix @ _np.array(xyz(x=0, y=0, z=1))
    return xyz(x=plane_x_unit_abs, y=plane_y_unit_abs, z=plane_z_unit_abs)

def gps_rel_positions(gps1: wgs84tup, gps2: wgs84tup):
    xyz_abs_1 = wgs84_to_ecef(wgs84=gps1)
    xyz_abs_2 = wgs84_to_ecef(wgs84=gps2)
    xyz_deltas_abs = delta_xyz(curr_xyz=xyz_abs_1, targ_xyz=xyz_abs_2)
    gps1_plane = gps_loc_plane_unit_vectors(gps_location=gps1)
    plane_x_val = gps1_plane.x @ xyz_deltas_abs
    plane_y_val = gps1_plane.y @ xyz_deltas_abs
    plane_z_val = gps1_plane.z @ xyz_deltas_abs
    pxyz = xyz(x=plane_x_val, y=plane_y_val, z=plane_z_val)
    angle_from_x_deg = _math.degrees(_math.atan2(pxyz.y, pxyz.x))  # y,x
    angle_from_y_deg = _math.degrees(_math.atan2(pxyz.z, pxyz.x))  # y,x
    radius = _math.sqrt(dot_product(pxyz, pxyz))
    return angle_from_x_deg, angle_from_y_deg, radius

if __name__ == '__main__':
    # center parking line north cement meridian end barrier
    lat1 = latlon(deg=47, minute=40, second=32.63, hemisphere='N')
    lon1 = latlon(deg=116, minute=47, second=43.07, hemisphere='W')
    elevation_m1 = 2139 * 0.3048  # ft * 0.3048 -> m
    gps1 = wgs84tup(
        latitude_rad=conv_deghms_2_radians(**lat1._asdict()),
        longitude_rad=conv_deghms_2_radians(**lon1._asdict()),
        elevation_m=elevation_m1,
    )

    # center parking line south cement meridian end barrier farthest east point
    lat2 = latlon(deg=47, minute=40, second=30.93, hemisphere='N')
    lon2 = latlon(deg=116, minute=47, second=42.54, hemisphere='W')
    elevation_m2 = 2140 * 0.3048  # ft * 0.3048 -> m
    gps2 = wgs84tup(
        latitude_rad=conv_deghms_2_radians(**lat2._asdict()),
        longitude_rad=conv_deghms_2_radians(**lon2._asdict()),
        elevation_m=elevation_m2,
    )

    rot_matrix = eulerAnglesToRotationMatrix(theta=[_math.pi/2,_math.pi/2,0])
    rotationMatrixToEulerAngles(R=rot_matrix)
    xyz(x=1,y=1,z=1)
    
    new_unit_vectors = gps_loc_plane_unit_vectors(gps_location=gps1)
    test = gps_rel_positions(gps1=gps1, gps2=gps2)
