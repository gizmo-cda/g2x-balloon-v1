#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
general object to handle two point heading

* note on surface normal: http://www.geo.hunter.cuny.edu/~jochen/GTECH201/Lectures/Lec6concepts/05%20-%20Understanding%20datums.html
* good article on wg84 history: https://frontierprecision.com/wp-content/uploads/EvolutionofWGS84andNAD83.pdf
* gps coordinates, guide to google maps verification: https://www.ubergizmo.com/how-to/read-gps-coordinates/

The simplest way to transform coordinates in Python is pyproj, i.e. the
Python interface to PROJ.4 library. https://gis.stackexchange.com/questions/78838/converting-projected-coordinates-to-lat-lon-using-python/78944#78944
"""
import pathlib as _pathlib
import inspect as _inspect
#import os as _os
import typing as _typing
import math as _math
import json as _json

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


def write_move_gps_state(fp_abs, gps):
    """
    Moves are atomic, writing a file is not.  Want to write to temp file and
    then move the file to the final file path absolute location.
    refer to https://realpython.com/python-pathlib/#reading-and-writing-files

    JSON + namedtuple
    https://stackoverflow.com/questions/28148260/writing-and-reading-namedtuple-into-a-file-in-python/28149664#28149664

    Interesting module but KISS for this instance
    https://github.com/ltworf/typedload
    """
    tmp_fp_abs = fp_abs.parent / f'tmp-{fp_abs.name:s}'
    state_text = _json.dumps(gps._asdict())  # uses ordered dict
    tmp_fp_abs.write_text(state_text)
    tmp_fp_abs.replace(fp_abs)  # deletes the tmp file

def read_gps_state(fp_abs):
    state_text = fp_abs.read_text()
    gps_pt = wgs84tup(**_json.loads(state_text))
    return gps_pt


class TwoGps(object):
    def __init__(self, state_dir=None, gps1=None, gps2=None):
        if state_dir is not None:
            self.state_dir = _pathlib.Path(state_dir)
        else:
            # modern py3.4+ way to get the __file__ directory
            # when running from site-packages can get irradic behavior
            # https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory
            filename = _inspect.getframeinfo(_inspect.currentframe()).filename
            self.state_dir = _pathlib.Path(filename).resolve().parent
            self.state_dir /= 'state_dir'

        if not self.state_dir.exists() and self.state_dir.parent.exists():
            self.state_dir.mkdir(parents=False, exist_ok=True)
        self.gps1_state_fpabs = self.state_dir / 'gps1_state.tsv'
        self.gps2_state_fpabs = self.state_dir / 'gps2_state.tsv'
        self.gps1 = gps1
        self.gps2 = gps2


    @property  # https://www.programiz.com/python-programming/property
    def gps1(self):
        return read_gps_state(fp_abs=self.gps1_state_fpabs)

    @property  # https://www.programiz.com/python-programming/property
    def gps2(self):
        return read_gps_state(fp_abs=self.gps2_state_fpabs)

    @gps1.setter  # https://www.programiz.com/python-programming/property
    def gps1(self, value):
        write_move_gps_state(fp_abs=self.gps1_state_fpabs, gps=value)

    @gps2.setter  # https://www.programiz.com/python-programming/property
    def gps2(self, value):
        write_move_gps_state(fp_abs=self.gps2_state_fpabs, gps=value)


if __name__ == '__main__':
    # center parking line north cement meridian end barrier
    lat1 = latlon(deg=47, minute=40, second=32.63, hemisphere='N')
    lon1 = latlon(deg=116, minute=47, second=43.07, hemisphere='W')
    elevation_ft1 = 2139  # ft
    _gps1 = wgs84tup(
        latitude_rad=conv_deghms_2_radians(**lat1._asdict()),
        longitude_rad=conv_deghms_2_radians(**lon1._asdict()),
        elevation_ft=elevation_ft1,
    )

    # center parking line south cement meridian end barrier farthest east point
    lat2 = latlon(deg=47, minute=40, second=30.93, hemisphere='N')
    lon2 = latlon(deg=116, minute=47, second=42.54, hemisphere='W')
    elevation_ft2 = 2140  # ft
    _gps2 = wgs84tup(
        latitude_rad=conv_deghms_2_radians(**lat2._asdict()),
        longitude_rad=conv_deghms_2_radians(**lon2._asdict()),
        elevation_ft=elevation_ft2,
    )

    tgps = TwoGps(gps1=_gps1, gps2=_gps2)
#    print(tgps.gps1_state_fpabs)
#    fp_abs = tgps.gps1_state_fpabs
#    gps = _gps1
