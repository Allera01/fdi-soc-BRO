### ANALISIS DE REDES SOCIALES

## Estudiantes:
- Mario Carrilero Sánchez
- Mario Gallego Hernández
- Diego Linares Espíldora
- Álvaro Llera Calderón

## P1 informacion de la pagina principal de [reddit españa](https://old.reddit.com/r/spain/)

# Informacion

ES un programa en Python que realiza el web scraping del subreddit r/spain para crear un conjunto de datos que contenga información sobree sta red social.

La informacion que vamos a obtener es la de la paguina principal de este subreddit: los posts, los comentarios de esos posts y los usuarios que han creado eso posts

La informacion de los post que vamos a guardar es: el titulo, la fecha, la descripcion textual (si la hay) y el autor.

La informacion de los comentarios que vamos a guardar es: el texto, la fecha, el post al que responde y el autor.

La informacion de los usuarios que vamos a guardar es: el nombre, el karma, los posts creados y los comentarios hechos

# Cómo instalar

TODO (poner como instalar las dependencias del pyproject y el uv)

# Cómo ejecutar

Una vez instalados ya se puede ejecutar el programa

Ejecuta en la linea de comandos de python:

  ~~~
  uv run main.py
  ~~~
  ~~~
  uv run analyze.py
  ~~~

Una vez ejecutado deberian aparecer en la carpeta 3 csv (usuarios.csv, posts.csv, comentarios.csv) con la informacion de la pagina principal de [reddit españa](https://old.reddit.com/r/spain/)
