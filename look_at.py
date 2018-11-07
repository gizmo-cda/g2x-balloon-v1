import pytest
import pdb
import math as _math
import typing as _typing
#import numpy as _np

class xyz(_typing.NamedTuple):
    x: float
    y: float
    z: float

class out_look_at(_typing.NamedTuple):
    angle_rad_between_unit_vectors: float
    unit_vector_axis_of_rotation: xyz
    unit_vector_to_target: xyz


def unit_vector_to_target(current_pos, target_pos):
    delta_x = float(target_pos.x - current_pos.x)
    delta_y = float(target_pos.y - current_pos.y)
    delta_z = float(target_pos.z - current_pos.z)
    print(f'delta_x: {delta_x:.5}')
    print(f'delta_y: {delta_y:.5}')
    print(f'delta_z: {delta_z:.5}')
    max_val = max([delta_x, delta_y, delta_z])
    return xyz(x=delta_x / max_val, y=delta_y / max_val, z=delta_z / max_val)

def dot_product(vect1, vect2):
    dot_sum = 0
    if len(vect1) != len(vect2) or len(vect1) == 0:
        raise IOError('somehting wrong')
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