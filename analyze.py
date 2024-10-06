from bs4 import BeautifulSoup
import csv
from pathlib import Path
import requests

f = Path("cache") / "index.html"
t = f.read_text()
p = "https://old.reddit.com/r/spain/comments/"
d = "https://old.reddit.com/user/"

soup = BeautifulSoup(t, 'html.parser')

datos_post = []
datos_usuarios = []
datos_comentario = []

for i in soup.findAll("div", {"class": "thing"}):
    #print("a")
    id_post = i["data-fullname"]
    titulo = (i.find("a", {"class": "title"})).text 
    aux = i.find("a", {"class": "author"})
    if aux:
        autor = aux.text
    else: 
        autor = "Autor desconocido"
    fecha = i.find("time")["title"]
    #print(aux.text)
    #print(autor)
    if aux:
        #print("h")
        j = requests.get(d + autor)
        soup3 = BeautifulSoup(j.content, 'html.parser') 
        
        post_usuario = []
        comentario_usuario = []
        
        karma = soup3.find("span", {"class": "karma"})
        #print(karma)
        for m in soup3.findAll("div", {"class": "thing"}):
            #print("u")
            #nombre_usuario = autor;
            #karma = soup3.find("span", {"class": "karma"}).get_text()
            #print(karma)
            post_usuario.append({
                'link': "https://old.reddit.com/" + m["data-permalink"]
            })
            
        datos_usuarios.append({
            'nombre': autor,
            'karma': karma,
            'post': post_usuario
        })
        '''datos_usuarios.append({
            'nombre': nombre_usuario,
            'karma': karma.get_text(),
            'posts': post_usuario,
            'comentarios': comentario_usuario
        })'''
            
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

l = 0
for z in range(0,len(datos_post)):
    #print(l)
    b = datos_post[l]['id_post']
    dir = b.lstrip('t3_')
    r = requests.get(p+dir)
    l = l +1
    soup2 = BeautifulSoup(r.content, 'html.parser')
    cuenta = 0
    for i in soup2.findAll("div", {"class": "thing"}):
        if cuenta>0:
            id_post = i["data-fullname"]
            aux = i.find("a", {"class": "author"})
            if aux:
                autor_post = aux.text
            else:
                autor_post = "Autor desconocido"
            fecha_comment = i.find("time")["title"]
            x = i.find("div", {"class": "md"})
            comentario = x.find('p').text
            datos_comentario.append({
                'comentario' : comentario,
                'fecha' : fecha_comment,
                'post al que responde': "t3_" + dir,
                'autor': autor_post
            })
        else:
            cuenta = cuenta +1

with open('posts.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['id_post', 'titulo', 'autor' ,'fecha','descripcion'])
    writer.writeheader()
    writer.writerows(datos_post)

with open('comentarios.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['comentario','fecha','post al que responde','autor'])
    writer.writeheader()
    writer.writerows(datos_comentario)

with open('usuarios.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['nombre', 'karma', 'post'])
    writer.writeheader() 
    writer.writerows(datos_usuarios)
