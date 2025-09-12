import http.server
import socketserver
import hashlib
import os
import email.utils

PORT = 8080
FILE = "index.html"


def get_headers():
    with open(FILE, "rb") as f:
        data = f.read()
    etag = hashlib.md5(data).hexdigest()
    last_mod = email.utils.formatdate(os.path.getmtime(FILE), usegmt=True)
    return data, etag, last_mod


def do_GET(self):
    if self.path not in ["/", "/index.html"]:
        self.send_error(404)
        return

    try:
        data, etag, last_mod = get_headers()

        inm = self.headers.get("If-None-Match")
        ims = self.headers.get("If-Modified-Since")

        if inm == etag or ims == last_mod:
            self.send_response(304)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_mod)
        self.end_headers()
        self.wfile.write(data)

    except FileNotFoundError:
        self.send_error(404)


# Patch handler method
http.server.SimpleHTTPRequestHandler.do_GET = do_GET

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()
