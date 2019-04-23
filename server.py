import http.server
import socketserver
import termcolor
import requests, sys

PORT = 8000


server = "http://rest.ensembl.org"
ext = "/info/species?"
r = requests.get(server + ext, headers={"Content-Type": "application/json"})
if not r.ok:
    r.raise_for_status()
    sys.exit()
decoded = r.json()
name = decoded['species']
result1 = []
result= ''
for i in name:
    n = str(i['common_name'])
    result1.append(n)
    result += "<p>{}</p>".format(n)



class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)

        species = self.path.split ('?')
        total_species = species[0]
        if len(species)== 2:
            number = species[1]
            number1 =number.split ('=')
            if len(number1) == 2:
                number2 =number1[1]


        if self.path == '/':
            f = open("form.html", 'r')
            contents = f.read()
        elif total_species == '/listSpecies':
            if number.endswith('='):
                contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>List of species</h1>
                        {}</p>
                        <a href="/">Link to main</a>""".format(result)
            else:
                resultt = result1[0:int(number2)]
                contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>List of species</h1>
                        {}</p>
                        <a href="/">Link to main</a>""".format(resultt)
        elif 

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