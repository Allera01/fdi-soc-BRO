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


# P2 Investigación en conjuntos de datos extraídos de [Twitter/X](https://x.com/)

## Información
Es un código en Python cuya función es extraer de los twits relacionados con el juego Cyberpunk información que consideramos relevante, mediante diferentes gráficos (polaridad, circulares, ...) en formato png.

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
uv add pandas matplotlib nltk textblob
~~~

## Cómo ejecutar
Una vez instalados ya se puede ejecutar el programa:
~~~
uv run main.py
~~~

## Ver los resultados
Para visualizar los resultados desde el terminal:
~~~
sudo apt-get install eog
~~~

Y, finalmente, para abrir el png:
~~~
eog <nombre del archivo>
~~~


# P3 Cálculos sobre redes libres de escala

## Información
Es un código Python cuyo objetivo es calcular distintas propiedades y estadísticas de redes sociales. Además, se elabora un pequeño informe comparando las redes y determinando si son libres de escala.
Optativamente, se calcularán medidas de conectividad basadas en caminos a través de estimaciones usando muestreo u otras técnicas imaginativas.

## Cómo instalar
// Parte de instalación de uv y librerías

### Click
Click es una biblioteca para Python que permite crear interfaces de línea de comandos de forma sencilla y eficiente. Proporciona decoradores que facilitan la creación de comandos, opciones y argumentos, haciendo que el código sea más legible y estructurado.

Para instalar Click, puedes usar pip:
~~~
pip install click
~~~
Una vez instalado, ya podemos manejar parámetros y argumentos en la línea de comandos.

### Black
Black es un formateador de código Python. Es una herramienta que permite formatear automáticamente tu código para que siga convenciones de estilo, lo que hace que el código sea más legible y consistente sin necesidad de ajustar el formato manualmente.

Para instalar Black, puedes usar pip:
~~~
pip install black
~~~

#### Uso de Black:
Puedes ejecutar Black en un archivo específico o en un directorio completo.
##### Para formatear un archivo:
~~~
black main.py
~~~
##### Para formatear todos los archivos Python en un directorio:
~~~
black .
~~~

## Ver los resultados:
Para mostrar las propiedades básicas de una red social, que viene descrita por su lista de aristas, deberemos pasar como argumento el fichero en que se detalla dicha información.
~~~
uv run main.py facebook.edgelist
~~~

De esta manera, estaremos accediendo a la información básica de la red social Facebook.
