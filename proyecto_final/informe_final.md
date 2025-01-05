# Informe sobre YouTube y el análisis de comentarios
## Autor: Mario Gallego Hernández, Mario Carrilero Sánchez, Diego Linares Espildora y Álvaro Llera Calderón.

![Imagen de la portada](https://www.ucm.es/data/cont/docs/3-2016-07-21-Marca%20UCM%20logo%20negro.png)

Este informe presenta una introducción sobre la plataforma **YouTube**, el análisis de los comentarios de los usuarios mediante la construcción de un grafo, y cómo extraer datos de esta plataforma utilizando la **API de Google**. A lo largo de este documento se justifica el uso de nodos y aristas para representar los comentarios y sus respuestas, además de un análisis sobre la estructura del código utilizado en el proyecto junto con los resultados obtenidos analizados. 

---

# Índice

1. [Introducción a YouTube](#introducción-a-youtube)
2. [Justificación de la Representación con Nodos y Aristas](#justificación-de-la-representación-con-nodos-y-aristas)
3. [Extracción de Datos con la API de YouTube](#extracción-de-datos-con-la-api-de-youtube)
4. [Explicación de la Estructura del Código](#explicación-de-la-estructura-del-código)
5. [Análisis de resultados obtenidos junto con breve conclusiones](#analisis-de-los-resultados)

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

#


