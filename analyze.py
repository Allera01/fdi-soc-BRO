from bs4 import BeautifulSoup
import csv
import requests
from pathlib import Path

f = Path("cache") / "index.html"
t = f.read_text()
p = "https://old.reddit.com/r/spain/comments/"

soup = BeautifulSoup(t, 'html.parser')
#print(soup.title)
#print(soup.get_text())
#for string in soup.strings:
   # print(repr(string))
#print(soup.prettify())

datos_post = []
datos_comentario = []

for i in soup.findAll("div", {"class": "thing"}):
    id_post = i["data-fullname"]
    id_pag = p + id_post[3:]
    titulo = (i.find("a", {"class": "title"})).text 
    aux = i.find("a", {"class": "author"})
    if aux:
        autor = aux.text
    else: 
        autor = "Autor desconocido"
    fecha = i.find("time")["title"]
    descripcion = (i.find("div", {"class": "md"}))
    datos_post.append({
        'id_post' : id_post,
        'titulo': titulo,
        'autor': autor,
        'fecha': fecha,
        'descripcion': descripcion
        })
r = requests.get(id_pag)
soup2 = BeautifulSoup(r.content, 'html.parser')

for i in soup.findAll("div", {"class": "thing"}):
    id_post = i["data-fullname"]
    titulo_post = (i.find("a", {"class": "title"})).text
    autor_post = i.find("a", {"class": "author"}).text
    fecha_comment = i.find("time")["title"]
    comentario = i.find("div", {"class": "md"})
    datos_comentario.append({
        'comentario' : comentario,
        'fecha' : fecha_comment,
        'post al que responde': titulo_post,
        'autor': autor_post
        })

print(id_pag)
print(datos_post)
print("-------------------------------------------")
print(datos_comentario)
