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
#import pathlib as _pathlib
#import inspect as _inspect
import typing as _typing
import math as _math
import numpy as _np
import math as math
import numpy as np
#import json as _json

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
    elevation_ft: float

class xyztup(_typing.NamedTuple):
    x: float
    y: float
    z: float

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
     
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))
 
    return R  # Rotation Matrix

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
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
 
    return np.array([x, y, z])


if __name__ == '__main__':
    # center parking line north cement meridian end barrier
    lat1 = latlon(deg=47, minute=40, second=32.63, hemisphere='N')
    lon1 = latlon(deg=116, minute=47, second=43.07, hemisphere='W')
    elevation_ft1 = 2139  # ft
    gps1 = wgs84tup(
        latitude_rad=conv_deghms_2_radians(**lat1._asdict()),
        longitude_rad=conv_deghms_2_radians(**lon1._asdict()),
        elevation_ft=elevation_ft1,
    )

    # center parking line south cement meridian end barrier farthest east point
    lat2 = latlon(deg=47, minute=40, second=30.93, hemisphere='N')
    lon2 = latlon(deg=116, minute=47, second=42.54, hemisphere='W')
    elevation_ft2 = 2140  # ft
    gps2 = wgs84tup(
        latitude_rad=conv_deghms_2_radians(**lat2._asdict()),
        longitude_rad=conv_deghms_2_radians(**lon2._asdict()),
        elevation_ft=elevation_ft2,
    )

    rot_matrix = eulerAnglesToRotationMatrix(theta=[_math.pi/2,_math.pi/2,0])
    rotationMatrixToEulerAngles(R=rot_matrix)
    xyztup(x=1,y=1,z=1)
