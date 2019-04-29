import http.server
import socketserver
import sys
import requests

PORT = 8000


def listpecies():
    server = "http://rest.ensembl.org"
    ext = "/info/species?"
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    decoded = r.json()
    name = decoded['species']
    result1 = []
    result = ''
    for i in name:
        n = str(i['name'])
        result1.append(n)
        result += "<p>{}</p>".format(n)
    return result, result1


def karyotype(specie):
    server = "http://rest.ensembl.org"
    ext = "/info/assembly/" + specie
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not r.ok:
        result = """requests.exceptions.HTTPError: 400 
        Client Error: Bad Request for url: http://rest.ensembl.org/info/assembly/""" + specie
        return result
    decoded = r.json()
    result = decoded['karyotype']
    return result


def length(specie, chromo):
    server = "http://rest.ensembl.org"
    ext = "/info/assembly/" + specie + "/" + chromo
    r = requests.get(server+ext, headers={"Content-Type": "application/json"})
    if not r.ok:
        result = """requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: http://rest.ensembl.org"""+ext
        return result
    decoded = r.json()
    length1 = decoded['length']
    return length1


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        global spe, chromosome, number2
        print(self.path)

        endpoint1 = ''
        l_endpoint = self.path.split('?')
        endpoint = l_endpoint[0]
        if len(l_endpoint) == 2:
            endpoint1 += str(l_endpoint[1])
            number1 = endpoint1.split('=')
            if len(number1) == 2:
                number2 = number1[1]
            number = endpoint1.split('&')
            if len(number) == 2:
                spe = number[0].lstrip('specie=')
                chromosome = number[1].lstrip('chromo=')
                print (spe, chromosome)

        if self.path == '/':
            f = open("form.html", 'r')
            contents = f.read()

        elif endpoint == '/listSpecies' or (self.path == '/listSpecies'):
            result, result1 = listpecies()
            if endpoint1.endswith('=') or (self.path == '/listSpecies'):
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
                r = ''
                resultt = result1[0:int(number2)]
                r += "</p><p>".join(resultt)
                contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>List of species</h1>
                        {}</p>
                        <a href="/">Link to main</a>""".format(r)

        elif endpoint == '/karyotype':
            if number2 == '':
                s = open("error.html")
                contents = s.read()
            else:
                contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>Karyotype of {}</h1>
                        {}</p>
                        <a href="/">Link to main</a>""".format(number2, karyotype(number2))

        elif endpoint == '/chromosomeLength':
            if chromosome != '' and spe != '':
                contents = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>RESULT</title>
                    </head>
                    <body>
                    <h1>Lenght of {} chromosome of the specie {}. </h1>
                    The lenght is: {}</p>
                    <a href="/">Link to main</a>""".format(chromosome, spe, length(spe, chromosome))
            else:
                s = open("error.html")
                contents = s.read()

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
