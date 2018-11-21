r"""
rest server module to interact with Google Earth and raspberry pi's.

Composed of a general object to the two points "states".  States represent
last updated position information from the raspberry pi's received through
posts.

Additionally composed of rest server that manages the http responses
accordingly.

* note on surface normal: http://www.geo.hunter.cuny.edu/~jochen/GTECH201/Lectures/Lec6concepts/05%20-%20Understanding%20datums.html
* good article on wg84 history: https://frontierprecision.com/wp-content/uploads/EvolutionofWGS84andNAD83.pdf


* gps coordinates, guide to google maps verification: https://www.ubergizmo.com/how-to/read-gps-coordinates/

The simplest way to transform coordinates in Python is pyproj, i.e. the
Python interface to PROJ.4 library. https://gis.stackexchange.com/questions/78838/converting-projected-coordinates-to-lat-lon-using-python/78944#78944


Want to be able to handle GET & POST requests.  So following
[Simple Python HTTP(S) Server With GET/POST Examples](https://blog.anvileight.com/posts/simple-python-http-server/).

Additional command line commands to get and post
curl -I http://localhost:8000
curl 'http://localhost:8000?foo=bar&bin=go'
curl -d "foo=bar&bin=go" http://localhost:8000

or using only python

    import json; import requests
    lat = '10 '; lat_compass = 'W'
    lng = '10 '; lng_compass = 'W'
    alt = '10 '
    url="http://10.10.107.188:8000/"
    header={'Content-Type': 'application/json' }
    data={
        'latitude': lat + lat_compass,
        'longiude': lng + lng_compass,
        'altitude': alt + 'm'
    }
    req = requests.post(url, headers=header, data=json.dumps(data))
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from io import BytesIO
import pathlib as _pathlib
import inspect as _inspect
import json as _json


import relpos as _relpos
import pdb

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

def kml_byte_str(gps1, gps2, ):
    """
    writes the KML Google Earth displays
    """
    #gps1 = latitude_rad, longitude_rad, elevation_m

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
       ) % (gps1.longitude_rad, gps1.latitude_rad)
    return kml

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
        self.gps1 = gps1
        if gps2 is None:
            gps2 = _relpos.wgs84tup(latitude_rad=0., longitude_rad=0., elevation_m=0.)
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

    def gen_kml_str(self):
        byte_str = kml_byte_str(gps1=self.gps1, gps2=self.gps2, )
        return byte_str



class StoreHandler(BaseHTTPRequestHandler):
    #store_path = pjoin(curdir, 'store.json')
    two_gps = TwoGps()
    # kml_bytes = two_gps.gen_kml_str().encode()

    def do_GET(self):
#        if self.path == '/gps_example.kml':
#            with open(self.store_path) as fh:
        self.send_response(200)
        self.send_header('Content-type', 'application/vnd.google-earth.kml+xml')
        #print 'Content-Type: application/vnd.google-earth.kml+xml\n'
        self.end_headers()
        # self.wfile.write(fh.read().encode())
        kml_bytes = self.two_gps.gen_kml_str().encode()
        self.wfile.write(kml_bytes)

    def do_POST(self):
#        if self.path == '/store.json':
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        json_str = data.decode()
        self.send_response(200)
        self.end_headers()

#        state_text = fp_abs.read_text()
#        json_dict = _json.loads(json_str)
#        gps_pt = wgs84tup(**json_dict)


#class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#
#    def do_GET(self):
#        self.send_response(200)
#        self.end_headers()
#        self.wfile.write(b'Hello, world!')
#
#    def do_POST(self):
#        content_length = int(self.headers['Content-Length'])
#        body = self.rfile.read(content_length)
#        self.send_response(200)
#        self.end_headers()
#        response = BytesIO()
#        response.write(b'This is POST request. ')
#        response.write(b'Received: ')
#        response.write(body)
#        self.wfile.write(response.getvalue())

if True and __name__ == '__main__':
    # center parking line north cement meridian end barrier
    lat1 = _relpos.latlon(deg=47, minute=40, second=32.63, hemisphere='N')
    lon1 = _relpos.latlon(deg=116, minute=47, second=43.07, hemisphere='W')
    elevation_m1 = 0.3048 * 2139  # ft/m * ft
    _gps1 = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**lat1._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**lon1._asdict()),
        elevation_m=elevation_m1,
    )

    # center parking line south cement meridian end barrier farthest east point
    lat2 = _relpos.latlon(deg=47, minute=40, second=30.93, hemisphere='N')
    lon2 = _relpos.latlon(deg=116, minute=47, second=42.54, hemisphere='W')
    elevation_m2 = 0.3048 * 2140  # ft/m * ft
    _gps2 = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**lat2._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**lon2._asdict()),
        elevation_m=elevation_m2,
    )

    tgps = TwoGps(gps1=_gps1, gps2=_gps2)
    lat1_rad = _gps1.latitude_rad
    lon1_rad = _gps1.longitude_rad
    lat2_rad = _gps2.latitude_rad
    lon2_rad = _gps2.longitude_rad


PORT = 8000
if False:
    httpd = HTTPServer(('localhost', PORT), StoreHandler)
    httpd.serve_forever()
elif True and __name__ == '__main__':
    with socketserver.TCPServer(
                # server_address=("127.0.0.1", PORT),
                server_address=("", PORT),
                RequestHandlerClass=StoreHandler,
                # directory=TWO_GPS.state_dir,
            ) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever(poll_interval=0.5)

#$ curl -X POST --data "one two three four" localhost:8080/store.json
#$ curl -X GET localhost:8080/store.json
#one two three four%
