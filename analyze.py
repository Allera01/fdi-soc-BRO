from bs4 import BeautifulSoup
import csv
from pathlib import Path
import requests

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
datos_usuarios = []
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
    #saca el texto de la descripcion de un post
    aux2 = i.find("div", {"class" : "expando"})
    if aux2:        
        data_content = aux2.get("data-cachedhtml")
            
        if data_content:
            cached_soup = BeautifulSoup(data_content, 'html.parser')
            aux3 = cached_soup.find('div', class_='md')
                                                                    
            if aux3:
                descripcion = aux3.get_text().strip()
            else:
                descripcion = "No hay descripcion"
        else:
            descripcion = "No hay descripcion"
    else:
        descripcion = "No hay descripcion"
    
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
    aux = i.find("a", {"class": "author"})
    if aux:
        autor_post = aux.text
    else:
        autor_post = "Autor desconocido"
    fecha_comment = i.find("time")["title"]
    comentario = i.find("div", {"class": "md"})
    datos_comentario.append({
        'comentario' : comentario,
        'fecha' : fecha_comment,
        'post al que responde': titulo_post,
        'autor': autor_post
    })

#print(id_pag)
#print(datos_post)
#print("-------------------------------------------")
#print(datos_comentario)

with open('posts.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['id_post', 'titulo', 'autor' ,'fecha','descripcion'])
    writer.writeheader()
    writer.writerows(datos_post)

#with open('comentarios.csv', 'w', newline='') as csvfile:
#    writer = csv.DictWriter(csvfile, fieldnames=['comentario','fecha','post al que responde','autor'])
#    writer.writeheader()
#    writer.writerows(datos_comentario)

#with open('usuarios.csv', 'w', newline='') as csvfile:
#    writer = csv.DictWriter(csvfile, fieldnames=[])
#    writer.writeheader() 
#    writer.writerow(datos_usuarios)
