# ANÁLISIS DE REDES SOCIALES

## Estudiantes
- Mario Carrilero Sánchez
- Mario Gallego Hernández
- Diego Linares Espíldora
- Álvaro Llera Calderón

# P1 Información de la página principal de [reddit españa](https://old.reddit.com/r/spain/)

## Información
Es un programa en Python que realiza el web scraping del subreddit r/spain para crear un conjunto de datos que contenga información sobre esta red social.

La información que obtenemos es la de la página principal de este subreddit: los posts, sus comentarios y los usuarios que han creado esos posts.

La información de los posts que guardamos es: el título, la fecha, la descripción textual (si la hay) y el autor.

La información de los comentarios que guardamos es: el texto, la fecha, el post al que responde y el autor.

La información de los usuarios que vamos a guardar es: el nombre, el karma, los posts creados y los comentarios hechos.

## Cómo instalar
Es necesario contar con un entorno de ejecución de Python.

Descargar y almacenar en una carpeta los archivos: **main.py**, **configuracion_p1.toml** y **analyze.py**. 

Abrir el terminal direccionada a esa carpeta.

Es necesario instalar uv:
~~~
pip install --user --break-system-packages uv
~~~

Para descargarse las librerías:
~~~
uv add bs4 bachoff requests pathlib networkx
~~~

## Cómo ejecutar
Una vez instalados ya se puede ejecutar el programa:
~~~
uv run main.py
~~~
~~~ 
uv run analyze.py
~~~

Una vez ejecutado, aparecen en la carpeta tres ficheros en formato csv (usuarios.csv, posts.csv, comentarios.csv) con la información de la página principal de [reddit españa](https://old.reddit.com/r/spain/)


# P2 Análisis de tuits sobre Cyberpunk

## Información
Es un código en Python cuya función es extraer, de los tuits relacionados con el juego Cyberpunk, información que consideramos relevante, mediante diferentes gráficos en formato png.

Todo lo analizado ha sido concluido en el archivo informe.pdf

## Cómo instalar
Es necesario contar con un entorno de ejecución de Python.

Descargar y almacenar en una carpeta los archivos: **main.py** de la carpeta practica_2, **cyberpunk.csv** que es el archivo a analizar.

Abrir el terminal direccionada a esa carpeta.

Es necesario instalar uv:
~~~
pip install --user --break-system-packages uv
~~~

Para descargarse las librerías:
~~~
uv add pandas matplotlib string seaborn Counter
~~~

## Cómo ejecutar
Una vez instalados ya se puede ejecutar el programa:
~~~
uv run main.py
~~~

## Ver los resultados
Para visualizar los gráficos en formato.png desde el terminal:
~~~
sudo apt-get install eog
eog <nombre del archivo>
~~~

Para generar el informe en formato .pdf:
~~~
pandoc informe.md -o informe.pdf
~~~

# P3 Cálculos sobre redes libres de escala

## Información
Es un código Python cuyo objetivo es calcular distintas propiedades y estadísticas de redes sociales. Además, se elabora un pequeño informe comparando las redes y determinando si son libres de escala.
Optativamente, se calcularán medidas de conectividad basadas en caminos a través de estimaciones usando muestreo u otras técnicas imaginativas.

## Cómo instalar
Es necesario contar con un entorno de ejecución de Python.

Descargar y almacenar en una carpeta los archivos: **main.py** de la carpeta practica_3 y los ficheros **lastfm.edgelist**, **facebook.edgelist**, **bitcoin.edgelist**, **congress.edgelist** que son los que vamos a analizar.

Abrir el terminal direccionada a esa carpeta.

Es necesario instalar uv:
~~~
pip install --user --break-system-packages uv
~~~

Para descargarse las librerías:
~~~
uv add networkx matplotlib click
~~~

## Cómo ejecutar
Para mostrar las propiedades básicas de una red social, que viene descrita por su lista de aristas, deberemos pasar como argumento el fichero en que se detalla dicha información.
~~~
uv run main.py facebook.edgelist
~~~

De esta manera, estaremos accediendo a la información básica de la red social Facebook.

Para mostar qué funcionalidades avanzadas hay disponibles, ejecute el comando:
~~~
uv run main.py --help
~~~

# Practica Final Analisis de Youtube

## Información
Es un código Python cuyo objetivo es descargar comentarios de YouTube y con ellos calcular distintas propiedades y estadísticas de la red social. Además, se ha elaborado un informe donde podemos observar las distintas gráficas que somos capaces de sacar y un pequeño análisis de estas. 

## Cómo instalar
Es necesario contar con un entorno de ejecución de Python.

Descargar y almacenar en una carpeta los archivos que se encuentran en la carpeta de proyectos final, si quieres no hace falta descargarte la caché, junto al archivo **pyproject.toml**.

Abrir el terminal direccionada a esa carpeta.

Es necesario instalar uv:
~~~
pip install --user --break-system-packages uv
~~~

Las librerías se descargarán  una vez ejecutemos el código por primera vez.

## Cómo ejecutar
Para comenzar con la ejecución es recomendable en un principio descargar los comentarios de un video mediante este comando:
~~~
uv run main.py -d
~~~

Una vez descargado los comentarios ya podremos ejecutar toda nuestra funcionalidad mediante el comando:
~~~
uv run main.py -a
~~~

O si bien quieres ejecutar la funcionalidad por parte, ejecute el comando:
~~~
uv run main.py --help
~~~
y seleccione el comando designado.
