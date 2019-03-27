# -*- coding: utf-8 -*-
"""
https://developers.google.com/kml/documentation/expiration

"""

import inspect as _inspect
import json as _json
import pathlib as _pathlib
import pytest
import typing as _typing

import relpos as _relpos


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
        if gps1 is None:
            gps1 = _relpos.wgs84tup(latitude_rad=0., longitude_rad=0., elevation_m=0.)
            gps1 = GizmoHq.ne_pt
        if gps2 is None:
            gps2 = _relpos.wgs84tup(latitude_rad=0., longitude_rad=0., elevation_m=0.)
            gps2 = GizmoHq.se_pt
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

    def gen_kml_byte_str(self):
#        byte_str = kml_byte_str(gps1=self.gps1, gps2=self.gps2, )
        kml_str = KML().make_kml_rev1(
            attenna_gps=self.gps1,
            balloon_gps=self.gps2,
        )
        byte_str = kml_str.encode()
        return byte_str



class GizmoHq():
    north_east_lat = _relpos.latlon(deg=47, minute=40, second=32.56, hemisphere='N')
    north_east_lon = _relpos.latlon(deg=116, minute=47, second=42.06, hemisphere='W')
    north_west_lat = _relpos.latlon(deg=47, minute=40, second=31.96, hemisphere='N')
    north_west_lon = _relpos.latlon(deg=116, minute=47, second=45.67, hemisphere='W')
    south_west_lat = _relpos.latlon(deg=47, minute=40, second=30.27, hemisphere='N')
    south_west_lon = _relpos.latlon(deg=116, minute=47, second=45.70, hemisphere='W')
    south_east_lat = _relpos.latlon(deg=47, minute=40, second=30.24, hemisphere='N')
    south_east_lon = _relpos.latlon(deg=116, minute=47, second=44.21, hemisphere='W')

    altitude_above_ground_m = 0.3048 * 100  # m/ft * ft

    ne_pt = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**north_east_lat._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**north_east_lon._asdict()),
        elevation_m=altitude_above_ground_m,
    )
    nw_pt = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**north_west_lat._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**north_west_lon._asdict()),
        elevation_m=altitude_above_ground_m,
    )
    sw_pt = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**south_west_lat._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**south_west_lon._asdict()),
        elevation_m=altitude_above_ground_m,
    )
    se_pt = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**south_east_lat._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**south_east_lon._asdict()),
        elevation_m=altitude_above_ground_m,
    )

    @classmethod
    def four_corners(cls):
        return (cls.ne_pt, cls.nw_pt, cls.sw_pt, cls.se_pt)

    @classmethod
    def coord_text_array(cls):
        return "\n".join([gps.google_earth_pts for gps in cls.four_corners()])



# f"""<?xml version="1.0" encoding="UTF-8"?>
#<kml xmlns="http://www.opengis.net/kml/2.2">
#<Document>
#  <name>Document.kml</name>
#  <open>1</open>
#  <Placemark>
#    <name>Document Feature 1</name>
#    <styleUrl>#exampleStyleDocument</styleUrl>
#    <Point>
#      <coordinates>-122.371,37.816,0</coordinates>
#    </Point>
#  </Placemark>
#  <Placemark>
#    <name>Document Feature 2</name>
#    <styleUrl>#exampleStyleDocument</styleUrl>
#    <Point>
#      <coordinates>-122.370,37.817,0</coordinates>
#    </Point>
#  </Placemark>
#</Document>
#</kml>"""
class KML():
    def __init__(
                self, docname:_typing.AnyStr=None,
                open_bool: _typing.Union[bool]=None,
             ):
        if not docname:
            self.docname = 'Gizmo2Extreme.kml'
        else:
            self.docname = docname
        if open_bool or open_bool is None:
            self.open_bool = 1
        else:
            self.open_bool = 0

    def make_kml_rev1(self, attenna_gps, balloon_gps, ):
        gps1, gps2 = attenna_gps, balloon_gps
        kml = f"""{self._header_str:s}
  <Placemark>
    <name>Antenna Location</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <altitudeMode>relativeToGround</altitudeMode>
    <Point>
      <!--- <coordinates>{gps1.latitude_rad:f},{gps1.longitude_rad:f},{gps1.elevation_m:f}</coordinates> -->
      <coordinates>{attenna_gps.google_earth_pts:s}</coordinates>
    </Point>
  </Placemark>
  <Placemark>
    <name>Balloon Location</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <altitudeMode>relativeToGround</altitudeMode>
    <Point>
      <!--- <coordinates>{gps2.latitude_rad:f},{gps2.longitude_rad:f},{gps2.elevation_m:f}</coordinates> -->
      <coordinates>{balloon_gps.google_earth_pts:s}</coordinates>
    </Point>
  </Placemark>
{self._trailer_str:s}"""
        return kml

    @property
    def _header_str(self):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>{self.docname:s}</name>
  <open>{self.open_bool:b}</open>
  <Style id="exampleStyleDocument">
    <LabelStyle>
      <color>ff0000cc</color>
    </LabelStyle>
  </Style>"""

    @property
    def _trailer_str(self):
        return f"""</Document>
</kml>"""

    

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
    gps_pt = _relpos.wgs84tup(**_json.loads(state_text))
    return gps_pt

def kml_byte_str_random(*args, **kwargs):
    """
    writes the KML Google Earth displays
    """
    #gps1 = latitude_rad, longitude_rad, elevation_m
    import random

    latitude = random.randrange(-90, 90)
    longitude = random.randrange(-180, 180)
    kml = (
       '<?xml version="1.0" encoding="UTF-8"?>\n'
       '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
       '<Placemark>\n'
       '<name>Random Placemark</name>\n'
       '<Point>\n'
       '<coordinates>%d,%d</coordinates>\n'
       '</Point>\n'
       '</Placemark>\n'
       '</kml>'
       ) %(longitude, latitude)
    return kml

def kml_byte_str(gps1, gps2, ):
    kml = \
f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>Document.kml</name>
  <open>1</open>
  <Style id="exampleStyleDocument">
    <LabelStyle>
      <color>ff0000cc</color>
    </LabelStyle>
  </Style>
  <Placemark>
    <name>Document Feature 1</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <Point>
      <coordinates>-122.371,37.816,0</coordinates>
    </Point>
  </Placemark>
  <Placemark>
    <name>Document Feature 2</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <Point>
      <coordinates>-122.370,37.817,0</coordinates>
    </Point>
  </Placemark>
</Document>
</kml>"""
    kml = \
f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>Document.kml</name>
  <open>1</open>
  <Style id="exampleStyleDocument">
    <LabelStyle>
      <color>ff0000cc</color>
    </LabelStyle>
  </Style>
  <Placemark>
    <name>Document Feature 1</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <Point>
      <coordinates>{gps1.latitude_rad:f},{gps1.longitude_rad:f},{gps1.elevation_m:f}</coordinates>
    </Point>
  </Placemark>
  <Placemark>
    <name>Document Feature 2</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <Point>
      <coordinates>{gps2.latitude_rad:f},{gps2.longitude_rad:f},{gps2.elevation_m:f}</coordinates>
    </Point>
  </Placemark>
</Document>
</kml>"""
    return kml
