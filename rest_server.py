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

import twogpspoints   # import TwoGps
import pdb
#pdb.set_trace()
PORT = 8000

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

if False:
    httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
    httpd.serve_forever()
elif __name__ == '__main__':
    # TWO_GPS = twogpspoints.TwoGps()
    with socketserver.TCPServer(
                # server_address=("127.0.0.1", PORT),
                server_address=("", PORT+1),
                RequestHandlerClass=SimpleHTTPRequestHandler,
                # directory=TWO_GPS.state_dir,
            ) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever(poll_interval=0.5)
        
#from os import curdir
#from os.path import join as pjoin
#
#from http.server import BaseHTTPRequestHandler, HTTPServer
#
#class StoreHandler(BaseHTTPRequestHandler):
#    store_path = pjoin(curdir, 'store.json')
#
#    def do_GET(self):
#        if self.path == '/store.json':
#            with open(self.store_path) as fh:
#                self.send_response(200)
#                self.send_header('Content-type', 'text/json')
#                self.end_headers()
#                self.wfile.write(fh.read().encode())
#
#    def do_POST(self):
#        if self.path == '/store.json':
#            length = self.headers['content-length']
#            data = self.rfile.read(int(length))
#
#            with open(self.store_path, 'w') as fh:
#                fh.write(data.decode())
#
#            self.send_response(200)
#
#
#server = HTTPServer(('', 8080), StoreHandler)
#server.serve_forever()
#
#$ curl -X POST --data "one two three four" localhost:8080/store.json
#$ curl -X GET localhost:8080/store.json    
#one two three four%