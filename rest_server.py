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
    url="http://10.10.107.98:8000/"
    url="http://localhost:8000/"
    print(requests.get(url, ).content.decode())
    lat = '10 '; lat_compass = 'W'
    lng = '10 '; lng_compass = 'W'
    alt = '10 '
    header={'Content-Type': 'application/json' }
    data={
        'latitude': lat + lat_compass,
        'longiude': lng + lng_compass,
        'altitude': alt + 'm'
    }
    req = requests.post(url, headers=header, data=json.dumps(data))
"""
import pytest
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from io import BytesIO
import pathlib as _pathlib


import relpos as _relpos
import kmlgps as _kmlgps
import pdb



class StoreHandler(BaseHTTPRequestHandler):
    #store_path = pjoin(curdir, 'store.json')
    two_gps = _kmlgps.TwoGps()
    # kml_bytes = two_gps.gen_kml_str().encode()

    def do_GET(self):
#        if self.path == '/gps_example.kml':
#            with open(self.store_path) as fh:
        self.send_response(200)
        self.send_header('Content-type', 'application/vnd.google-earth.kml+xml')
        #print 'Content-Type: application/vnd.google-earth.kml+xml\n'
        self.end_headers()
        # self.wfile.write(fh.read().encode())
        kml_bytes = self.two_gps.gen_kml_byte_str()
#        self.wfile.write(b"hey GET this code")
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

if False and __name__ == '__main__':
    # center parking line north cement meridian end barrier
    lat1 = _relpos.latlon(deg=47, minute=40, second=32.63, hemisphere='N')
    lon1 = _relpos.latlon(deg=116, minute=47, second=43.07, hemisphere='W')
    elevation_m1 = 0.3048 * 2139  # m/ft * ft
    _gps1 = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**lat1._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**lon1._asdict()),
        elevation_m=elevation_m1,
    )

    # center parking line south cement meridian end barrier farthest east point
    lat2 = _relpos.latlon(deg=47, minute=40, second=30.93, hemisphere='N')
    lon2 = _relpos.latlon(deg=116, minute=47, second=42.54, hemisphere='W')
    elevation_m2 = 0.3048 * 2140  # m/ft * ft
    _gps2 = _relpos.wgs84tup(
        latitude_rad=_relpos.conv_deghms_2_radians(**lat2._asdict()),
        longitude_rad=_relpos.conv_deghms_2_radians(**lon2._asdict()),
        elevation_m=elevation_m2,
    )

    tgps = _kmlgps.TwoGps(gps1=_gps1, gps2=_gps2)
    lat1_rad = _gps1.latitude_rad
    lon1_rad = _gps1.longitude_rad
    lat2_rad = _gps2.latitude_rad
    lon2_rad = _gps2.longitude_rad

if False and __name__ == '__main__':  # gizmo-cda building polygon
    north_east_lat = _relpos.latlon(deg=47, minute=40, second=32.56, hemisphere='N')
    north_east_lon = _relpos.latlon(deg=116, minute=47, second=42.06, hemisphere='W')
    north_west_lat = _relpos.latlon(deg=47, minute=40, second=31.96, hemisphere='N')
    north_west_lon = _relpos.latlon(deg=116, minute=47, second=45.67, hemisphere='W')
    south_west_lat = _relpos.latlon(deg=47, minute=40, second=30.27, hemisphere='N')
    south_west_lon = _relpos.latlon(deg=116, minute=47, second=45.70, hemisphere='W')
    south_east_lat = _relpos.latlon(deg=47, minute=40, second=30.24, hemisphere='N')
    south_east_lon = _relpos.latlon(deg=116, minute=47, second=44.21, hemisphere='W')
    altitude_above_ground_m = 0.3048 * 100  # m/ft * ft
#    pytest.set_trace()
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
    coord_text_array = "\n".join([gps.google_earth_pts for gps in (ne_pt, nw_pt, sw_pt, se_pt)])
    print(coord_text_array)


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
