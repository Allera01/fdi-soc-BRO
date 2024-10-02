Mario Carrilero Sanchez, mcarri17@ucm.es

Mario Gallego Hernandez, margal15@ucm.es

Diego Linares Espildora, dielinar@ucm.es

Alvaro Llera Calderon, allera01@ucm.es

## 1- YouTube

**Nodos y Aristas**

- Nodos: usuarios / vídeos

- Nodos temporales: directos (se acaban convirtiendo en vídeos)

- Aristas: suscripción / comentarios / compartir / descripción / recomendaciones

NO VAMOS A UTILIZAR LA API DEBIDO A LA OBLIGACIÓN DE NÚMEROS DE TELÉFONO REALES

**Analisis de contenido**: utilizando web scrapping podemos obtener datos como: 

- Información de los canales junto con redes sociales asociadas.

- Comentarios (junto con los canales de cada comentario) y Likes de los vídeos del canal.

- Correo electrónico.


## 1- Tiktok

**Nodos y Aristas**

- Nodos: Usuario / Videos

- Nodos Temporales: Directos

- Aristas: Comentarios / Compartir / Bibliotecas / Mensajeria privada

**Analisis de contenido**: este contenido se puede sacar desde la api de tiktok teniendo una cuenta de Tiktok for developers, solo se puede sacar informacion de  perfiles y videos publicos

- perfiles: se puede sacar ID, imagen avatar, nombre, etc

- videos seleccionados por el usuario (propios)

- videos seleccionados por el usuario (de la aplicacion en general)

**Aspectos topológicos**:

- Se puede sacar la informacion completa de los videos: Id, numero de likes, fecha de creacion, numero de comentarios,  duracion,  etc.

- Se puede sacar informacion relacionada con los anuncios: cada cuantos videos salta un anuncio, restricciones del anuncio por paises, la pagina web del anunciante


## 2- Kick

**Nodos y Aristas**

- Nodos: Usuarios / Canales

- Nodos Temporales: Directos (se acaban convirtiendo en videos)
  
- Aristas: Chat del directos / Mensajes Privados

**Analisis de contenido**:

- Información de los canales junto con redes sociales asociadas.

- Comentarios (junto con los canales de cada comentario)

- Los videos pertenecientes al canal

La api de Kick pide correo de empresa y un proceso de selección antes de poder recibirla (no recomendado)

## 3- Twitch

Practicamente igual que kick pero se puede acceder a su api con un correo electronico
