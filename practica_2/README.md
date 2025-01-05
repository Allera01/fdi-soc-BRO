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
