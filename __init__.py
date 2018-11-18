import os
import http.server as server
import socketserver

PORT = int(os.environ.get('FILE_DEPOSITORY_PORT', 8000))

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def do_PUT(self):
        path = os.path.abspath(os.path.basename(self.path))
        if os.path.exists(path):
            response = 'file already exists'
        else:
            with open(path, 'wb') as file:
                file.write(self.rfile.read(int(self.headers['Content-Length'])))
            response = 'wrote {}'.format(path)
        print(response)
        self.wfile.write(response.encode('utf-8'))

with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
    print('serving on port {}'.format(PORT))
    httpd.serve_forever()
