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

### Cómo instalar

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

### Cómo ejecutar

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

### Información

Es un código en python cuya función es extraer de los twits relacionados con el juego cyberpunk información que nosotros consideremos relevante. Esto lo hace mediante
diferentes gráficos (polaridad, circulares, ...).

Como ya he mencionado toda la información extraída se guarda en diferentes gráficos y estos a su vez tienen formato png.

Todo lo analizado lo hemos ido concluyendo en el archivo informe.pdf

### Cómo instalar

Es necesario contar con un entorno de ejecución de Python.

Descargar y almacenar en una carpeta los archivos: **main.py** de la carpeta practica_2, **cyberpunk.csv** que es el archivo a analizar.

Abrir el terminal direccionada a esa carpeta y ejecutar el comando:

Para empezar hay que descargarse uv:

~~~
pip install --user --break-system-packages uv
~~~

Para descargarse las librerías:

~~~
uv add pandas matplotlib nltk textblob
~~~

### Cómo ejecutar

Una vez instalados ya se puede ejecutar el programa.

Ejecutar el programa en uv:

~~~
uv run main.py
~~~

### Ver los resultados

Para visualizar los resultados nosotros los hemos abierto en **vscode**, pero también se pueden visualizar desde el terminal ejecutando primero:

~~~
sudo apt-get install eog
~~~

Y finalmente para abrir el png se ejecuta:

~~~
eog <nombre del archivo>
~~~

## P3 Cálculos sobre redes libres de escala

### Información

Es un código python cuyo objetivo es calcular distintas propiedades y estadísticas de redes sociales. Además, se elabora un pequeño informe comparando las redes y determinando si son libres de escala.
Optativamente, se calcularán medidas de conectividad basadas en caminos a través de estimaciones usando muestreo u otras técnicas imaginativas.

### Cómo instalar

// Parte de instalación de uv y librerías

#### Click

Click es una biblioteca para Python que permite crear interfaces de línea de comandos de forma sencilla y eficiente. Proporciona decoradores que facilitan la creación de comandos, opciones y argumentos, haciendo que el código sea más legible y estructurado.

Para instalar Click, puedes usar pip:
~~~
pip install click
~~~
