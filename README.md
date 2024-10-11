### ANALISIS DE REDES SOCIALES

## Estudiantes:
- Mario Carrilero Sánchez
- Mario Gallego Hernández
- Diego Linares Espíldora
- Álvaro Llera Calderón

## P1 informacion de la pagina principal de [reddit españa](https://old.reddit.com/r/spain/)

# Informacion

Es un programa en Python que realiza el web scraping del subreddit r/spain para crear un conjunto de datos que contenga información sobree sta red social.

La informacion que vamos a obtener es la de la paguina principal de este subreddit: los posts, los comentarios de esos posts y los usuarios que han creado eso posts

La informacion de los post que vamos a guardar es: el titulo, la fecha, la descripcion textual (si la hay) y el autor.

La informacion de los comentarios que vamos a guardar es: el texto, la fecha, el post al que responde y el autor.

La informacion de los usuarios que vamos a guardar es: el nombre, el karma, los posts creados y los comentarios hechos

# Cómo instalar

Hay que tener un entorno de ejecucion de python

Descargar y almacenar en una carpeta los archivos: **main.py**, **configuracion_p1.toml**, **analyze.py** y **requerimientos.txt**. 

Abrir el terminal direccionada a esa carpeta y ejecutar el comando:

  ~~~
Para empezar hay que descargarse uv: pip install --user --break-system-packages uv
  ~~~

uv add bs4 bachoff requests pathlib networkx

# Cómo ejecutar

Una vez instalados ya se puede ejecutar el programa

Ejecuta en la linea de comandos de python:

  ~~~
  python main.py
  ~~~
  ~~~
  python analyze.py
  ~~~
o si tienes instalado python3
  ~~~
  python3 main.py
  ~~~
  ~~~
  python3 analyze.py
  ~~~
Para ejecutar el programa en uv: uv run main.py seguido de uv run analyze.py

Una vez ejecutado deberian aparecer en la carpeta 3 csv (usuarios.csv, posts.csv, comentarios.csv) con la informacion de la pagina principal de [reddit españa](https://old.reddit.com/r/spain/)
