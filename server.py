import http.server
import socketserver
import termcolor

import requests, sys
server = "http://rest.ensembl.org"
ext = "/info/species?"
r = requests.get(server + ext, headers={"Content-Type": "application/json"})
if not r.ok:
    r.raise_for_status()
    sys.exit()
decoded = r.json()
name = decoded['species']
for i in name rang:
    n =i['common_name']
    print(n)

print (len(n))


PORT = 8000

class TestHandler(http.server.BaseHTTPRequestHandler):



    def do_GET(self):


        if self.path == '/' or self.path == '/favicon.ico':
            f = open("form.html", 'r')
            contents = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Lenght', len(str.encode(contents)))
            self.end_headers()

        #-- SEnding the body of the response message
            self.wfile.write(str.encode(contents))

        else:
            s = open("error.html")
            contents = s.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Lenght', len(str.encode(contents)))
            self.end_headers()
            # -- SEnding the body of the response message
            self.wfile.write(str.encode(contents))

# -- Main program
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT: {}".format(PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

print("The server is closed")