from bs4 import BeautifulSoup
import csv
from pathlib import Path

f = Path("cache") / "index.html"
t = f.read_text()

soup = BeautifulSoup(t, 'html.parser')
#print(soup.title)
#print(soup.get_text())
#for string in soup.strings:
   # print(repr(string))
#print(soup.prettify())

datos_post = []

for i in soup.findAll("div", {"class": "thing"}):
    id_post = i["data-fullname"]
    titulo = (i.find("a", {"class": "title"})).text 
    aux = i.find("a", {"class": "author"})
    if aux:
        autor = aux.text
    else: 
        autor = "Autor desconocido"
    fecha = i.find("time")["title"]
    descripcion = (i.find("div", {"class": "expando"}))
    datos_post.append({
        'id_post' : id_post,
        'titulo': titulo,
        'autor': autor,
        'fecha': fecha,
        'descripcion': descripcion
        })
