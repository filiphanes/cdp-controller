import http.server
import socketserver
import urllib.request
import urllib.parse

# run chromium --remote-debugging-port 9222 ...
CDP_ENDPOINT = "http://localhost:9222"

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            with open('index.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        elif self.path.startswith('/json'):
            # Proxy request to CDP endpoint
            with urllib.request.urlopen(CDP_ENDPOINT + self.path) as response:
                self.send_response(response.status)
                self.send_header('Content-type', response.headers.get('Content-Type'))
                self.end_headers()
                self.wfile.write(response.read())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith('/json'):
            request = urllib.request.Request(CDP_ENDPOINT + self.path, method='POST')
            with urllib.request.urlopen(request) as response:
                self.send_response(response.status)
                self.send_header('Content-type', response.headers.get('Content-Type'))
                self.end_headers()
                self.wfile.write(response.read())
        else:
            self.send_error(404)

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print("Server started at port", PORT)
        httpd.serve_forever()
