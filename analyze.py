from bs4 import BeautifulSoup
import backoff
import time
import csv
from pathlib import Path
import requests

dir_cache = Path("cache")
f = dir_cache / "index.html"
t = f.read_text(encoding='utf-8', errors='ignore')
p = "https://old.reddit.com/r/spain/comments/"
d = "https://old.reddit.com/user/"

soup = BeautifulSoup(t, "html.parser")

datos_post = []
autores_guardados = set()
datos_usuarios = []
datos_comentario = []

RATE_LIMIT_CALLS = 2
RATE_LIMIT_PERIOD = 1


@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=10)
def llamada_reddit(url):
    time.sleep(1)
    response = requests.get(url)
    response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
    return response


for i in soup.findAll("div", {"class": "thing"}):
    id_post = i["data-fullname"]
    titulo = (i.find("a", {"class": "title"})).text
    aux = i.find("a", {"class": "author"})
    if aux:
        autor = aux.text
    else:
        autor = "Autor desconocido"
    fecha = i.find("time")["title"]
    # si se conoce el autor del post se busca y se saca un link a sus post y comentarios mas recientes
    if aux:
        # se excluye los autores que ya estan guardados
        if autor not in autores_guardados:
            cache_file = dir_cache / (autor + ".html")
            # se buca el autor en el html, si no esta lo descarga de reddit
            if not Path.exists(cache_file):
                j = llamada_reddit(d + autor)
                cache_file.write_text(j.text, encoding='utf-8', errors='ignore')
                soup3 = BeautifulSoup(j.content, "html.parser")
            else:
                lol = cache_file.read_text(encoding='utf-8', errors='ignore')
                soup3 = BeautifulSoup(lol, "html.parser")
            # se descartan los autores que tengan la cuenta en privado
            h = soup3.find("meta", {"name": "robots"})
            if not h:
                post_usuario = []
                comentario_usuario = []

                karma = soup3.find("span", {"class": "karma"})
                for m in soup3.findAll("div", {"class": "thing"}):
                    if "link" in m.get("class", []):
                        post_usuario.append(
                            {
                                "link al post": "https://old.reddit.com/"
                                + m["data-permalink"]
                            }
                        )
                    elif "comment" in m.get("class", []):
                        comentario_usuario.append(
                            {
                                "link al comentario": "https://old.reddit.com/"
                                + m["data-permalink"]
                            }
                        )

                # guarda la informacion del usuario
                datos_usuarios.append(
                    {
                        "nombre": autor,
                        "karma": karma.get_text(),
                        "posts": post_usuario,
                        "comentarios": comentario_usuario,
                    }
                )

            autores_guardados.add(autor)

    # saca el texto de la descripcion de un post
    aux2 = i.find("div", {"class": "expando"})
    if aux2:
        data_content = aux2.get("data-cachedhtml")
        if data_content:
            cached_soup = BeautifulSoup(data_content, "html.parser")
            aux3 = cached_soup.find("div", class_="md")

            if aux3:
                descripcion = aux3.get_text().strip()
            else:
                descripcion = "No hay descripcion"
        else:
            descripcion = "No hay descripcion"
    else:
        descripcion = "No hay descripcion"

    # guarda la informacion del post
    datos_post.append(
        {
            "id_post": id_post,
            "titulo": titulo,
            "autor": autor,
            "fecha": fecha,
            "descripcion": descripcion,
        }
    )

# l sirve para recorrer todos los post que tengamos guardados y sacamos sus comentarios
l = 0
usernuevo = 0
for z in range(0, len(datos_post)):
    b = datos_post[l]["id_post"]
    # se quita el 't3_' del id_post para buscar adecuadamente el post
    dir = b.lstrip("t3_")
    cache_file = dir_cache / (b + ".html")
    # se buca el post en el html, si no esta lo descarga de reddit
    if not Path.exists(cache_file):
        r = llamada_reddit(p + dir)
        cache_file.write_text(r.text, encoding='utf-8', errors='ignore')
        soup2 = BeautifulSoup(r.content, "html.parser")
    else:
        lol = cache_file.read_text(encoding='utf-8', errors='ignore')
        soup2 = BeautifulSoup(lol, "html.parser")
    l = l + 1
    # cuenta sirve para saltarse el primer thing del post, que es el propio post
    cuenta = 0
    for i in soup2.findAll("div", {"class": "thing"}):
        if cuenta > 0:
            # se descarta los que no sean comentarios
            if "comment" in i.get("class", []):
                # se descarta los que estan eliminados
                if not "deleted" in i.get("class", []):
                    id_post = i["data-fullname"]
                    aux = i.find("a", {"class": "author"})
                    if aux:
                        autor_post = aux.text
                    else:
                        autor_post = "Autor desconocido"
                    if (autor_post not in autores_guardados) and (usernuevo < 50):
                      cache_file = dir_cache / (autor_post + ".html")
                      # se buca el autor en el html, si no esta lo descarga de reddit
                      if not Path.exists(cache_file):
                        j = llamada_reddit(d + autor_post)
                        cache_file.write_text(j.text, encoding='utf-8', errors='ignore')
                        soup3 = BeautifulSoup(j.content, "html.parser")
                      else:
                         lol = cache_file.read_text(encoding='utf-8', errors='ignore')
                         soup3 = BeautifulSoup(lol, "html.parser")
                      # se descartan los autores que tengan la cuenta en privado
                      h = soup3.find("meta", {"name": "robots"})
                      if not h:
                         post_usuario = []
                         comentario_usuario = []

                         karma = soup3.find("span", {"class": "karma"})
                         for m in soup3.findAll("div", {"class": "thing"}):
                             if "link" in m.get("class", []):
                                 post_usuario.append(
                                 {
                                  "link al post": "https://old.reddit.com/"
                                  + m["data-permalink"]
                                 }
                               )
                             elif "comment" in m.get("class", []):
                                 comentario_usuario.append(
                                 {
                                  "link al comentario": "https://old.reddit.com/"
                                  + m["data-permalink"]
                                 }
                              )
                        
                         # guarda la informacion del usuario
                         usernuevo = usernuevo  + 1
                         print(usernuevo)
                         datos_usuarios.append(
                         {
                            "nombre": autor_post,
                            "karma": karma.get_text(),
                            "posts": post_usuario,
                            "comentarios": comentario_usuario,
                          }
                        )

                      autores_guardados.add(autor_post)

                      fecha_comment = i.find("time")["title"]
                      x = i.find("div", {"class": "md"})
                      comentario = x.find("p").text
                      # guarda la informacion del comentario
                      datos_comentario.append(
                        {
                            "comentario": comentario,
                            "fecha": fecha_comment,
                            "link al post al que responde": "https://old.reddit.com/"
                            + i["data-permalink"],
                            "autor": autor_post,
                        }
                    )

        else:
            cuenta = cuenta + 1

# Crea y escribe el .csv de los comentarios
with open("comentarios.csv", "w", newline="", encoding='utf-8', errors='ignore') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=["comentario", "fecha", "link al post al que responde", "autor"],
    )
    writer.writeheader()
    writer.writerows(datos_comentario)

# Crea y escribe el .csv de los usuarios
with open("usuarios.csv", "w", newline="", encoding='utf-8', errors='ignore') as csvfile:
    writer = csv.DictWriter(
        csvfile, fieldnames=["nombre", "karma", "posts", "comentarios"]
    )
    writer.writeheader()
    writer.writerows(datos_usuarios)

# Crea y escribe el .csv de los posts
with open("posts.csv", "w", newline="", encoding='utf-8', errors='ignore') as csvfile:
    writer = csv.DictWriter(
        csvfile, fieldnames=["id_post", "titulo", "autor", "fecha", "descripcion"]
    )
    writer.writeheader()
    writer.writerows(datos_post)
