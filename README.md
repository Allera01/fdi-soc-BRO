# ANÁLISIS DE REDES SOCIALES

## Estudiantes:
- Mario Carrilero Sánchez
- Mario Gallego Hernández
- Diego Linares Espíldora
- Álvaro Llera Calderón

## P1 información de la página principal de [reddit españa](https://old.reddit.com/r/spain/)

### Información

Es un programa en Python que realiza el web scraping del subreddit r/spain para crear un conjunto de datos que contenga información sobre esta red social.

La información que vamos a obtener es la de la página principal de este subreddit: los posts, sus comentarios y los usuarios que han creado esos posts.

La información de los posts que vamos a guardar es: el título, la fecha, la descripción textual (si la hay) y el autor.

La información de los comentarios que vamos a guardar es: el texto, la fecha, el post al que responde y el autor.

La información de los usuarios que vamos a guardar es: el nombre, el karma, los posts creados y los comentarios hechos.

# Cómo instalar

Es necesario contar con un entorno de ejecución de Python.

Descargar y almacenar en una carpeta los archivos: **main.py**, **configuracion_p1.toml** y **analyze.py**. 

Abrir el terminal direccionada a esa carpeta y ejecutar el comando:

Para empezar hay que descargarse uv:

~~~
pip install --user --break-system-packages uv
~~~

Para descargarse las librerías:

~~~
uv add bs4 bachoff requests pathlib networkx
~~~

# Cómo ejecutar

Una vez instalados ya se puede ejecutar el programa.

Ejecutar el programa en uv:

~~~
uv run main.py
~~~
~~~ 
uv run analyze.py
~~~


Una vez ejecutado deberían aparecer en la carpeta tres ficheros en formato csv (usuarios.csv, posts.csv, comentarios.csv) con la información de la página principal de [reddit españa](https://old.reddit.com/r/spain/)

## P2 investigación en conjuntos de datos extraídos de [Twitter/X](https://x.com/)
