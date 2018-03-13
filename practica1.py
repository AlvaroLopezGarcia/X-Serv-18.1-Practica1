#!/usr/bin/python3

import webapp
import os

urlsReales = {}
urlsAcortadas = {}

FORMULARIO = """
    <form action= "/" Method= "POST">
    URL:<br>
    <input type="text" name="URL" ><br>
    <input type="submit" value="Enviar">
</form>
"""

def checkUrl(url):
    if url.startswith("http%3A%2F%2F"):
        return "http://" + url.split("%3A%2F%2F")[1]
    elif url.startswith("https%3A%2F%2F"):
        return "https://" + url.split("%3A%2F%2F")[1]
    else:
        return "http://" + url

def add(url, num):
    urlsAcortadas[num] = url
    urlsReales[url] = num

def writeFiLe(dictionary):
    resultado = ''
    archivo = open("practica1urls.csv", 'w')
    for i in dictionary:
        resultado += str(i) +','+ dictionary[i] +'\n'
    archivo.write(resultado)
    archivo.close()

def buscaUrl(url):
    found= False
    if url != '':
        url = checkUrl(url)
        for i in urlsAcortadas:
            if urlsAcortadas[i] == url and urlsReales[url] == i:
                found= True
                break
        if found != True or len(urlsAcortadas) == 0:
            add(url, len(urlsAcortadas))
            writeFiLe(urlsAcortadas)

def printDictionary():
    resultado = ''
    for i in urlsAcortadas:
        resultado +='<a href= ' + urlsAcortadas[i] +'>'+str(i) +','+ urlsAcortadas[i] +'</a><br/>'
    return resultado

def readFile():
    resultado = ''
    if (os.path.isfile("practica1urls.csv")):
        archivo = open("practica1urls.csv")
        for linea in archivo.readlines():
            if linea != '\n':
                num,url = linea.split(",")
                url = url.split("\n")[0]
                add(url, num)
    else:
        archivo = open("practica1urls.csv",'w')
    archivo.close()

class myWebapp(webapp.webApp):
    def parse(self, request):
        return (request.split()[0],request.split()[1],request)

    def process(self,parsedRequest):
        metodo,llave,peticion = parsedRequest
        if metodo == 'POST':
            cuerpo = peticion.split('\r\n\r\n',1)[1]            
            url = cuerpo.split('=')[1]
            buscaUrl(url)
        if llave == '/':
            codigo = "200 OK"
            respuesta = "<html><body><h1>" + FORMULARIO + "</h1><p>"+ printDictionary() +"</p></body></html>"
        elif llave == '/favicon.ico':
            codigo = "404 Not found"
            respuesta = "<html><body><h1>" + FORMULARIO + "</h1><p>"+ printDictionary() +"</p></body></html>"
        else:
            try:
                num = int(llave.split('/')[1])
            except ValueError:
                codigo = "404 Not found"
                respuesta = "<html><body><h1>Not found!!</h1></body></html>"
                return(codigo, respuesta)
            try:
                codigo = "302 HTTP REDIRECT"
                respuesta = "<html><head><meta http-equiv=Refresh content=0;url="+urlsAcortadas[num]+"></head></html>"
            except KeyError:
                codigo = "404 HTTP ERROR Recurso no disponible"
                respuesta = "<html><body><h1>" + FORMULARIO + "</h1><p>"+ printDictionary() +"</p></body></html>"
        return(codigo, respuesta)

    def __init__(self, hostname, port):
        readFile()
        super().__init__("localhost",1234)

if __name__ == "__main__":
    myapp = myWebapp("localhost",1234)
    
