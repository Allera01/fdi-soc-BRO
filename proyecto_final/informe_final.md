% Informe sobre YouTube y el análisis de comentarios
% Autor: Mario Gallego Hernández, Mario Carrilero Sánchez, Diego Linares Espildora y Álvaro Llera Calderón.

# Portada

Este informe presenta una introducción sobre la plataforma **YouTube**, el análisis de los comentarios de los usuarios mediante la construcción de grafos, y cómo extraer datos de esta plataforma utilizando la **API de Google**. A lo largo de este documento se justifica el uso de nodos y aristas para representar los comentarios y sus respuestas, además de un análisis sobre la estructura del código utilizado en el proyecto junto con los resultados obtenidos analizados. 

---

# Índice

1. [Introducción a YouTube](#introducción-a-youtube)
2. [Justificación de la Representación con Nodos y Aristas](#justificación-de-la-representación-con-nodos-y-aristas)
3. [Extracción de Datos con la API de YouTube](#extracción-de-datos-con-la-api-de-youtube)
4. [Explicación de la Estructura del Código](#explicación-de-la-estructura-del-código)
5. [Análisis de Resultados obtenidos junto con breve Conclusiones](#analisis-de-los-resultados)

---

# Introducción a YouTube

**YouTube** es una de las plataformas más populares a nivel mundial para la visualización y compartición de videos. Fundada en 2005 y adquirida por Google en 2006, YouTube ha crecido exponencialmente y actualmente alberga una gran cantidad de contenido generado por usuarios, que varía desde entretenimiento hasta educación. Los usuarios pueden interactuar con los videos mediante comentarios, "me gusta", "no me gusta", y suscripciones a canales.

La interacción de los usuarios, especialmente a través de los comentarios, crea una red de conversaciones que puede ser analizada para obtener valiosa información sobre las preferencias y comportamientos de la audiencia.

---

# Justificación de la Representación con Nodos y Aristas

En este informe, se utiliza un modelo de **grafo** para representar la interacción de los usuarios en los comentarios de los videos de YouTube. Este modelo se justifica de la siguiente manera:

- **Nodos**: Los nodos representan a los usuarios que comentan en un video. Cada usuario es un punto de interacción dentro de la red de comentarios, y sus interacciones están relacionadas con los comentarios que hacen o las respuestas que reciben.
  
- **Aristas**: Las aristas representan las respuestas que un usuario da a otro comentario. Así, una arista conecta el usuario de un comentario con el usuario de otro comentario al que responde.

Este enfoque tiene como objetivo modelar la interacción entre los usuarios y su influencia sobre otros, similar a cómo se construyen las redes sociales.

# Extracción de Datos con la API de Youtube

## Limitaciones del Scraping

Empezamos haciendo **scraping** en vez de la API ya que para la API necesitas unos credenciales que no teníamos. Tras extraer HTML con comentarios de vídeos de Youtube, nos dimos cuenta de que no eramos capaces de sacar más de una cantidad muy limitada de comentarios y nos era imposible sacar las respuestas de los comentarios. Este conjunto de datos fue considerado como insuficiente por el grupo y el scraping fue descartado por la falta de contenido esencial para hacer este trabajo. La API permite acceder a **toda la información**, incluyendo tanto los comentarios como las respuestas de los mismos.

## Requisitos para la API

Para utilizar la API de YouTube, es necesario contar con los siguientes elementos:

- Una **cuenta de Google**.
- Un **proyecto** en la [Google Developer Console](https://console.developers.google.com/).
- Una **clave de API** de YouTube Data API v3.

Además en necesario la siguiente librería de Python:

- `google-api-python-client`

El resultado del uso de la API, a diferencia de con scraping, es un **archivo JSON** con todos los comentarios, sus respuestas, los 'me gustas' que tiene cada comentarios e información adicional que utilizamos para analizar estos comentarios.

# Explicación de la Estructura del Código

Tras explicar como se extraen los datos con la API, mostraremos una breve explicación de los módulos que utilizamos.

## Descarga de Comentarios y Respuestas de un video de Youtube (descarga.py)

Este script en Python utiliza la **clave de YouTube Data API v3** para obtener los comentarios y respuestas de un video de YouTube proporcionado a través de su URL. El código permite almacenar los comentarios en formato **JSON**. Utilizamos bibliotecas como googleapiclient.discovery para interactuar con la API v3 y realizar solicitudes de datos y json para guardar estos comentarios y las respuestas en JSON. Al llamar a la función **descargar** creamos un directorio cache si no está creado previamente y se extrae la ID del video a partir de la URL que pedimos. Esta función llama a **sacar_comentarios** que se encarga de:
- **Obtener los detalles del video**: Llama a `obtener_detalles_video` para obtener el título y el canal del video.
- **Crea un directorio para almacenar los comentarios**: Utiliza la biblioteca `pathlib` para crear una ruta de almacenamiento basada en el nombre del canal y el título del video, asegurándose de que el directorio exista.
- **Consulta los comentarios**: Llama a `obtener_comentarios` para obtener los comentarios y respuestas del video.
- **Guarda los comentarios en un archivo JSON**: Si los comentarios no han sido guardados previamente, los almacena en un archivo JSON con el nombre ajustado al título del video.

Este script es útil para descargar comentarios y respuestas de un video de YouTube de manera eficiente utilizando la YouTube Data API. El manejo de directorios y archivos JSON asegura que los comentarios se almacenen de manera organizada y se evite la descarga redundante de comentarios si ya existen archivos guardados previamente.

## Carga de Comentarios desde un archivo JSON (cargar.py)

Este script en Python está diseñado para cargar y leer los comentarios descargados previamente en formato JSON a través de la YouTube Data API. Utiliza la estructura de directorios creada en el proceso de descarga para listar los canales y videos disponibles, permitiendo al usuario seleccionar cuál desea cargar. 
La función principal que coordina la carga de comentarios de un video es **cargar** y se encarga de:
- **Listar canales**: Llama a `listar_canales()` para obtener todos los canales disponibles en el directorio de caché.
- **Seleccionar un canal**: Permite al usuario seleccionar un canal de la lista proporcionada.
- **Listar videos del canal seleccionado**: Llama a `listar_videos()` para obtener los videos del canal seleccionado.
- **Seleccionar un video**: Permite al usuario seleccionar un video de la lista de videos del canal.
- **Cargar el video seleccionado**: Lee el archivo JSON del video seleccionado utilizando `read_text()` para cargar los comentarios y respuestas guardados en dicho archivo.

Este script proporciona una interfaz sencilla para cargar comentarios y respuestas de un video de YouTube previamente descargados en formato JSON. Utiliza un sistema de directorios organizado por canales y videos para que el usuario pueda navegar y seleccionar fácilmente el video que desea cargar. Es una herramienta útil para acceder y visualizar los comentarios almacenados sin tener que volver a descargarlos.

## Extracción de Comentarios con Respuestas desde JSON (extract.py)

Este script en Python tiene como objetivo extraer los comentarios de YouTube que tienen al menos una respuesta a partir de un archivo JSON previamente descargado y cargado. Los comentarios extraídos incluyen tanto los comentarios principales como las respuestas, y la información relacionada con estos comentarios se almacena en un formato estructurado.
La función principal es **extract_comments_from_json** y se encarga de:
- **Conversión del JSON**: Si la entrada es una cadena (`str`), se convierte en un diccionario de Python utilizando la función `json.loads()`.
- **Inicialización de la Lista de Comentarios**:Se inicializa una lista vacía `comments` donde se almacenarán los comentarios que tengan al menos una respuesta.
- **Verificación de la Estructura del JSON**: La función verifica si el JSON recibido es una lista. Si no es una lista, se imprime una advertencia.
Si es una lista, itera sobre los objetos dentro de ella, verificando que contengan la clave `'items'`.
- **Extracción de Comentarios y Respuestas**: Solo se agregan a la lista de resultados los comentarios que tengan al menos una respuesta. Para cada comentario principal con respuestas, se construye un diccionario `comment_info` que incluye:
     - **Autor del comentario**
     - **Texto del comentario**
     - **Fecha de publicación**
     - **Número de "likes"**
     - **Respuestas**: Lista con la información de las respuestas, si las hay.
- **Devolución de Resultados**: La función retorna la lista `comments`, que contiene todos los comentarios con al menos una respuesta.

Este script es útil para extraer comentarios que no solo provienen de los usuarios, sino que también tienen interacción (respuestas) en los videos de YouTube. Esto es particularmente valioso cuando se desea analizar o procesar comentarios que generan discusión, y puede ser útil en análisis de sentimientos, estudios de interacción social en plataformas de video o simplemente para obtener datos de interacción más ricos.

## Análisis semántico de los Comentarios de Youtube (analisis.py)

Este código tiene como objetivo analizar los comentarios de un video de YouTube, extrayendo datos sobre la polaridad (sentimiento) de los comentarios, la cantidad de "likes" y la cantidad de respuestas. Además, genera varios gráficos que visualizan estos datos. Recibe los comentarios previamente extraidos en extract.py y los analiza en varias funciones:
-**Obtener polaridad**: Utiliza `TextBlob` para calcular la polaridad de un texto, que varía entre -1 (negativo) y 1 (positivo). Utilizada por el resto de funciones.
-**Generar gráficos**: Genera varios gráficos basados en los comentarios extraídos desde un archivo JSON. Estos gráficos son:
    -**Polaridad vs Likes**: Un gráfico de dispersión que muestra la relación entre la polaridad de los comentarios y la cantidad de "likes".
    -**Respuestas en Comentarios Positivos vs Negativos**: Un gráfico de barras que compara la cantidad de respuestas en comentarios positivos y negativos.
    -**Likes vs Fecha de Publicación**: Un gráfico de líneas que muestra la evolución de los "likes" con respecto a la fecha de publicación de los comentarios.
-**Filtrar y Analizar palabras**: Filtra los comentarios que contienen la palabra "video" y calcula la polaridad de estos comentarios.
-**Graficar la evolución de la palabra**: Genera un gráfico que muestra la evolución de la polaridad de los comentarios que contienen la palabra "video" a lo largo del tiempo.

## Análisis y Visualización de Grafos (grafo.py)

Este código permite analizar las interacciones entre autores de comentarios y respuestas en un conjunto de datos JSON de YouTube. Crea y visualiza un grafo que conecta a los autores de los comentarios con los autores de las respuestas. Recibe los comentarios previamente extraidos y los analiza en varias funciones:
-**Analiza polaridad**: Utiliza `TextBlob` para calcular la polaridad de un texto, que varía entre -1 (negativo) y 1 (positivo). Utilizada por el resto de funciones.
-**Genera el grafo**: Carga los datos desde un archivo JSON y genera el tipo de grafo especificado.
-**Graficar grafos**: Grafica el grafo generado utilizando la librería `networkx`. Personaliza el layout y los nodos según el tipo de relación (autor o respuesta), y guarda la visualización como un archivo de imagen.
-**Crear un grafo analizando la actividad del autor**: Crea un grafo dirigido que conecta autores de comentarios con autores de respuestas. Los nodos son los autores, y las aristas representan la interacción entre los autores del comentario original y las respuestas.
-**Guardar el grafo dirigido**: Guarda el grafo dirigido en formato `.edgelist` en el directorio actual, si el archivo no existe.

## Estudio completo del grafo (analisis_grafos.py)

Este conjunto de funciones en Python está diseñado para el análisis y la visualización de grafos. Utiliza la biblioteca **NetworkX** para la manipulación de grafos y **Matplotlib** para la visualización. Además, implementa métricas y estadísticas relacionadas con Youtube. A continuación, se detallan las principales funciones del código y su propósito. Las funcionalidad principales son:
-**Calcular nodos y aristas de un grafo**: Calcula y muestra el número de nodos y aristas de un grafo. Esta función es útil para obtener una visión general del tamaño del grafo.
-**Calcular la distribución de los grados**: Calcula y visualiza la distribución de los grados de los nodos, guarda un gráfico de barras que muestra la distribución de grados, destacando los "hubs" (nodos con alto grado).
-**Calcular el coeficiente de clustering**: Calcula manualmente el coeficiente de clustering para cada nodo del grafo. El coeficiente de clustering mide la tendencia de los nodos a formar triángulos (conexiones entre los vecinos).
-**Visualizar la distribución de los coeficientes de clustering**: Esta función agrupa los coeficientes de clustering en intervalos y los visualiza en dos grupos: hubs y no hubs.
-**Visualizar la red**: Genera una visualización de la red destacando muchos hubs. Esta función crea una visualización destacando los hubs de la red, lo que puede ser útil para analizar las estructuras principales del grafo.
-**Calcular la distancia media**: Calcula la distancia media entre pares aleatorios de nodos en el grafo. Mide qué tan lejos están, en promedio, los nodos entre sí. Esta métrica puede ser útil para evaluar la "conectividad" global de la red.
-**Calcular el diametro**: Mide la distancia más larga en el grafo, lo que da una idea de la "expansión" del grafo.
-**Calcular la distancia a hub**: Analiza cómo los nodos se encuentran distribuidos en relación con los hubs de la red.








