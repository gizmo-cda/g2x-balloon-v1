r"""
Want to be able to handle GET & POST requests.  So following 
[Simple Python HTTP(S) Server With GET/POST Examples](https://blog.anvileight.com/posts/simple-python-http-server/).

Additional command line commands to get and post
curl -I http://localhost:8000
curl 'http://localhost:8000?foo=bar&bin=go'
curl -d "foo=bar&bin=go" http://localhost:8000
"""
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO


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


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
