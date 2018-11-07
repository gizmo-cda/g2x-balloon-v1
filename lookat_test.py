import pytest
import pdb
import look_at as xyp
import math as _math
import typing as _typing
#import numpy as _np

if __name__ == '__main__':
    pytest.main([
        __file__,
#        '-v',
        '--capture=sys',
        '-m developing',
    ])

@pytest.mark.developing
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


@pytest.mark.developing
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

if True and __main__ == '__main__':
    import numpy as _np
    n_look_vec = _np.matrix([0,1,0]).T
    def rot_matrix(rot_ang_deg):
        rot_ang_rad = _math.radians(rot_ang_deg)
        rot = _np.matrix([
            [_math.cos(rot_ang_rad), -_math.sin(rot_ang_rad),0],
            [_math.sin(rot_ang_rad), _math.cos(rot_ang_rad),0],
            [0,                     0,                     -1],
        ])
        return rot
    wnt = rot_matrix(30) @ n_look_vec
    