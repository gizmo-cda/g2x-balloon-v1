r"""
Want to be able to handle GET & POST requests.  So following
[Simple Python HTTP(S) Server With GET/POST Examples](https://blog.anvileight.com/posts/simple-python-http-server/).

Additional command line commands to get and post
curl -I http://localhost:8000
curl 'http://localhost:8000?foo=bar&bin=go'
curl -d "foo=bar&bin=go" http://localhost:8000
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from io import BytesIO
import json as _json

import twogpspoints   # import TwoGps
import pdb

PORT = 8000

class StoreHandler(BaseHTTPRequestHandler):
    #store_path = pjoin(curdir, 'store.json')
    two_gps = twogpspoints.TwoGps()
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

        state_text = fp_abs.read_text()
        json_dict = _json.loads(json_str)
        gps_pt = wgs84tup(**json_dict)


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

if False:
    httpd = HTTPServer(('localhost', PORT), StoreHandler)
    httpd.serve_forever()
elif False and __name__ == '__main__':
    with socketserver.TCPServer(
                # server_address=("127.0.0.1", PORT),
                server_address=("", PORT+1),
                RequestHandlerClass=StoreHandler,
                # directory=TWO_GPS.state_dir,
            ) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever(poll_interval=0.5)

#from os import curdir
#from os.path import join as pjoin
#
#from http.server import BaseHTTPRequestHandler, HTTPServer
#
#
#server = HTTPServer(('', 8080), StoreHandler)
#server.serve_forever()
#
#$ curl -X POST --data "one two three four" localhost:8080/store.json
#$ curl -X GET localhost:8080/store.json
#one two three four%