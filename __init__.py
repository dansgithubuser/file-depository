import os
import http.server as server
import socketserver

PORT = int(os.environ.get('FILE_DEPOSITORY_PORT', 8000))
PASSWORD = os.environ.get('FILE_DEPOSITORY_PASSWORD')

DIR = os.path.dirname(os.path.realpath(__file__))

# test
# server: `FILE_DEPOSITORY_PASSWORD=hunter2 python3 __init__.py`
# client: `curl -v -X POST -H "Authorization: hunter2" --data-binary @__init__.py localhost:8000/asdf`

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if PASSWORD and self.headers['Authorization'] != PASSWORD:
            self.send_error(404)
            return
        path = os.path.join(DIR, os.path.basename(self.path))
        if os.path.exists(path):
            self.send_error(400)
            return
        with open(path, 'wb') as file:
            file.write(self.rfile.read(int(self.headers['Content-Length'])))
        self.send_response(200)
        self.end_headers()
        self.wfile.write('OK'.encode('utf-8'))

with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
    print('serving on port {}'.format(PORT))
    httpd.serve_forever()
