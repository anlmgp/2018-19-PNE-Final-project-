import http.server
import socketserver
import sys
import requests
from Seq import Seq

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
        result1.append('<ul><li value="1">{}</li></ul>'.format(n.capitalize()))
        result += '<ul><li value="1">{}</li></ul>'.format(n.capitalize())
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
    result = ''
    r = decoded['karyotype']
    if len(r) == 0:
        result = 'No available karyotype.'
        return result
    else:
        for i in r:
            n = str(i)
            result += '<ul><li value="1">{}</li></ul>'.format(n.capitalize())
        return result


def humangene(gene):
    server = "http://rest.ensembl.org"
    ext = "/xrefs/symbol/homo_sapiens/" + gene
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not r.ok:
        result = """requests.exceptions.HTTPError: 400 
                Client Error: Bad Request for url: http://rest.ensembl.org/xrefs/symbol/homo_sapiens/""" + gene
        return result
    decoded = r.json()
    if len(decoded) == 0:
            result = """requests.exceptions.HTTPError: 400 
                    Client Error: Bad Request for url: http://rest.ensembl.org/xrefs/symbol/homo_sapiens/""" + gene
            return result
    if len(decoded) == 1:
        id = decoded[0]
        result = id['id']
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


def infogene(id):
    server = "http://rest.ensembl.org"
    ext = "/sequence/id/" + id
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    decoded = r.json()
    if len(decoded) == 1:
        result = """requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: http://rest.ensembl.org/sequence/id/""" + id
        return {'Result': result}
    else:
        sequence = decoded['seq']
        chrom = decoded['desc']
        n = chrom.split('chromosome:')
        n = n[1].split(':')
        chro = n[1]
        start2 = n[2]
        end2 = n[3]
        return {'Seq': len(sequence), 'Chromosome': chro, 'Start': start2, 'End': end2}


def calcgene(id):
    server = "http://rest.ensembl.org"
    ext = "/sequence/id/" + id
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    decoded = r.json()
    if len(decoded) == 1:
        result = """requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: http://rest.ensembl.org/sequence/id/""" + id
        return {'Result': result}
    else:
        sequence = decoded['seq']
        chrom = decoded['desc']
        n = chrom.split('chromosome:')
        n = n[1].split(':')
        chro = n[1]
        start1 = n[2]
        end1 = n[3]
        return {'Seq': sequence, 'Chromosome': chro, 'Start': start1, 'End': end1}


def listgene(chro, start3, end3):
    server = "http://rest.ensembl.org"
    ext = "/overlap/region/human/{}:{}-{}?feature=gene".format(chro, start3, end3)
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not r.ok:
        result = """requests.exceptions.HTTPError:400 Client Error: Bad Request for url: http://rest.ensembl.org""" + ext
        return result
    decoded = r.json()
    result = ''
    for i in decoded:
        result += '<ul><li value="1">{}</li></ul>'.format(i['external_name']) + '\n'
    return result


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        global spe, chromosome, number2, contents, end, chromoso, start
        print(self.path)

        endpoint1 = ''
        l_endpoint = self.path.split('?')
        endpoint = l_endpoint[0]
        print(endpoint)
        if len(l_endpoint) == 2:
            endpoint1 += str(l_endpoint[1])
            number1 = endpoint1.split('=')
            print(number1)
            if len(number1) == 2:
                number2 = number1[1]
            number = endpoint1.split('&')
            print(number)
            if len(number) == 2:
                spe = number[0][7:]
                chromosome = number[1][7:]
                print(spe, chromosome)
            elif len(number1) == 4:
                chromoso = number1[1][:-6]
                start = number1[2][:-4]
                end = number1[3]

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
                    <h1>List of species:</h1>
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
                    <h1>List of species:</h1>
                    {}</p>
                    <a href="/">Link to main</a>""".format(r)

        elif endpoint == '/karyotype':
            if number2 == '':
                s = open("error_input.html")
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
                    The sequence of the specie is: {}</p>
                    <a href="/">Link to main</a>""".format(chromosome, spe, length(spe, chromosome))

            else:
                s = open("error_input.html")
                contents = s.read()

        elif endpoint == '/geneSeq':
            if number2 == '':
                s = open("error_input.html")
                contents = s.read()
            else:
                contents = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>RESULT</title>
                    </head>
                    <body>
                    <h1>The sequence of the gene {}. </h1>
                    The sequence is: {}</p>
                    <a href="/">Link to main</a>""".format(number2, humangene(number2))

        elif endpoint == '/geneInfo':
            if number2 == '':
                s = open("error_input.html")
                contents = s.read()
            else:
                if len(infogene(humangene(number2))) == 1:
                    error = infogene(humangene(number2))
                    contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>The information of the gene {}. </h1>
                        The lenght of the sequence is: {}</p>
                        The chromosome of the gene is: {}</p>
                        The id of the gene is: {}</p>
                        Start position: {}</p>
                        End position: {}</p>
                        <a href="/">Link to main</a>""".format(number2,
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],)

                else:
                    contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>The information of the gene {}. </h1>
                        The lenght of the sequence is: {}</p>
                        The chromosome of the gene is: {}</p>
                        The id of the gene is: {}</p>
                        Start position: {}</p>
                        End position: {}</p>
                        <a href="/">Link to main</a>""".format(number2, infogene(humangene(number2))['Seq'],
                                                               infogene(humangene(number2))['Chromosome'],
                                                               humangene(number2),
                                                               infogene(humangene(number2))['Start'],
                                                               infogene(humangene(number2))['End'])

        elif endpoint == '/geneCalc':
            if number2 == '':
                s = open("error_input.html")
                contents = s.read()
            else:
                if len(calcgene(humangene(number2))) == 1:
                    error = calcgene(humangene(number2))
                    contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>The information of the gene {}. </h1>
                        The lenght of the sequence is: {} </p>
                        The A percentage is : {}</p>
                        The C percentage is: {}</p>
                        The T percentage is: {}</p>
                        The G percentage is: {}</p>
                        <a href="/">Link to main</a>""".format(number2,
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:],
                                                               (error['Result'])[0:105] + (error['Result'])[246:], )
                else:
                    gene = calcgene(humangene(number2))
                    sequence = Seq(gene['Seq'])
                    contents = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>RESULT</title>
                        </head>
                        <body>
                        <h1>The information of the gene {}. </h1>
                        The lenght of the sequence is: {} </p>
                        The A percentage is : {}%</p>
                        The C percentage is: {}%</p>
                        The T percentage is: {}%</p>
                        The G percentage is: {}%</p>
                        <a href="/">Link to main</a>""".format(number2, sequence.len(),
                                                               sequence.perc('A'),
                                                               sequence.perc('C'),
                                                               sequence.perc('T'),
                                                               sequence.perc('G'))

        elif endpoint == '/geneList':
            if chromoso == '' or start == '' or end == '':
                s = open("error_input.html")
                contents = s.read()
            else:
                contents = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>RESULT</title>
                    </head>
                    <body>
                    <h1>List of names of in location of gene:</h1>
                    {}</p>
                    <a href="/">Link to main</a>""".format(listgene(chromoso, start, end))

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
