import pytest
import pdb
import look_at as xyp
import math as _math
import math as math
import typing as _typing
import numpy as _np
import numpy as np

if __name__ == '__main__':
    pytest.main([
        __file__,
#        '-v',
        '--capture=sys',
        '-m developing',
    ])

#@pytest.mark.developing
def test_xyz_posxyz():
    pt1 = xyp.xyz(x=10, y=10, z=10)
    pt2 = xyp.xyz(x=10, y=20, z=10)
    pytest.set_trace()
    out_la = xyp.look_at(
        current_pos=pt1, target_pos=pt2,
        current_view_unit=xyp.xyz(x=1, y=0, z=0),
    )
    
    assert f'{out_la.angle_rad_between_unit_vectors:.10f}' == f'{_math.radians(90):.10f}'
    assert out_la.unit_vector_axis_of_rotation == xyp.xyz(x=0, y=0, z=-1)
    assert out_la.unit_vector_to_target== xyp.xyz(x=0, y=1, z=0)


def test_xyz_posxyz():
    pt1 = xyp.xyz(x=100, y=-100, z=100)
    pt2 = xyp.xyz(x=50, y=200, z=1000)
    pytest.set_trace()
    sq2ov2 = _math.sqrt(2)/2.    
    out_la = xyp.look_at(
        current_pos=pt1, target_pos=pt2,
        current_view_unit=xyp.xyz(x=-sq2ov2, y=sq2ov2, z=sq2ov2),
    )
    rot_deg = out_la.angle_rad_between_unit_vectors * 180 / _math.pi

    rot_x_euler = xyp.dot_product(
        vect1=out_la.unit_vector_axis_of_rotation,
        vect2=xyp.xyz(x=1, y=0, z=0)
    ) * rot_deg
    rot_y_euler = xyp.dot_product(
        vect1=out_la.unit_vector_axis_of_rotation,
        vect2=xyp.xyz(x=0, y=1, z=0)
    ) * rot_deg
    rot_z_euler = xyp.dot_product(
        vect1=out_la.unit_vector_axis_of_rotation,
        vect2=xyp.xyz(x=0, y=0, z=1)
    ) * rot_deg

    print(out_la.unit_vector_axis_of_rotation)
    assert f'{out_la.angle_rad_between_unit_vectors:.10f}' == f'{_math.radians(90):.10f}'
    assert out_la.unit_vector_axis_of_rotation == xyp.xyz(x=0, y=0, z=-1)
    assert out_la.unit_vector_to_target== xyp.xyz(x=0, y=1, z=0)

def rot_matrix_about_x(rot_ang_deg):
    rot_ang_rad = _math.radians(rot_ang_deg)
    rot = _np.matrix([
        [1,                     0,                     0  ],
        [0,_math.cos(rot_ang_rad), -_math.sin(rot_ang_rad)],
        [0,_math.sin(rot_ang_rad), _math.cos(rot_ang_rad) ],
    ])
    return rot

def rot_matrix_about_y(rot_ang_deg):
    rot_ang_rad = _math.radians(rot_ang_deg)
    rot = _np.matrix([
        [1,                     0,                     0  ],
        [0,_math.cos(rot_ang_rad), -_math.sin(rot_ang_rad)],
        [0,_math.sin(rot_ang_rad), _math.cos(rot_ang_rad) ],
    ])
    return rot

def rot_matrix_about_z(rot_ang_deg):
    rot_ang_rad = _math.radians(rot_ang_deg)
    rot = _np.matrix([
        [_math.cos(rot_ang_rad), -_math.sin(rot_ang_rad), 0],
        [_math.sin(rot_ang_rad),  _math.cos(rot_ang_rad), 0],
        [0,                       0,                      1],
    ])
    return rot

@pytest.mark.developing
@pytest.mark.parametrize("prior_loc, rot_deg, expected", [
    ([1,1,1], -45, [_math.sqrt(2),0,1]),
    ([1,0,1], 90, [0,1,1]),
    ([0,0,1], 20, [0,0,1]),
    ([1,1,1], 180, [-1,-1,1]),
])
def test_rotate_about_z(prior_loc, rot_deg, expected):
    """
    https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    """
    n_look_vec = _np.matrix(prior_loc).T
    rec = rot_matrix_about_z(rot_deg) @ n_look_vec
    exp = _np.matrix(expected).T
    assert _np.isclose(a=rec, b=exp, rtol=1e-05, atol=1e-08, equal_nan=True).all()


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


rot_matrix = eulerAnglesToRotationMatrix(theta=[_math.pi/2,_math.pi/2,0])
rotationMatrixToEulerAngles(R=rot_matrix)

if True and __name__ == '__main__':
    n_look_vec = _np.matrix([1,1,0]).T
    def rot_matrix_about_z(rot_ang_deg):
        rot_ang_rad = _math.radians(rot_ang_deg)
        rot = _np.matrix([
            [_math.cos(rot_ang_rad), _math.sin(rot_ang_rad),0],
            [_math.sin(rot_ang_rad), _math.cos(rot_ang_rad),0],
            [0,                     0,                     1],
        ])
        return rot
    wnt = rot_matrix_about_z(-45) @ n_look_vec
    