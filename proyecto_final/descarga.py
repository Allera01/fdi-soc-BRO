                                                                                                                                                                                                           
import googleapiclient.discovery 
import json
import asyncio
from pathlib import Path
from pyppeteer import launch
import re 


dir_cache = Path("cache")

# Función para obtener los comentarios de un video
def obtener_comentarios(youtube, video_id):
    comentarios = []
    request = youtube.commentThreads().list(
        part="snippet, replies",
        videoId=video_id,
        textFormat="plainText"
    )
    
    response = request.execute()
    
    # Se pueden agregar más lógica para extraer los comentarios de la respuesta si es necesario.
    return response

def extraer_video_id(url):
    # Expresión regular para detectar el ID del video en diferentes formatos de URL
    regex = r"(?:https?://(?:www\.)?youtube\.com/.*[?&]v=|https?://youtu\.be/|https?://m\.youtube\.com/v/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)  # El video ID está en el primer grupo de la expresión regular
    else:
        raise ValueError("No se pudo extraer el ID del video de la URL.")




def obtener_detalles_video(youtube, video_id):
    """
    Obtiene el nombre del video y el canal que lo creó.

    Args:
        youtube: Objeto autenticado de la API de YouTube (build de googleapiclient).
        video_id: ID del video para consultar.

    Returns:
        Una tupla con el título del video y el nombre del canal.
    """
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    if "items" in response and len(response["items"]) > 0:
        snippet = response["items"][0]["snippet"]
        titulo = snippet["title"]
        canal = snippet["channelTitle"]
        return titulo, canal
    else:
        raise ValueError("No se pudo obtener los detalles del video.")




def sacar_comentarios(video_id):
    # Configuración de la API
    api_key = 'AIzaSyAKa2JQhSNHvmzjqa1zr99niVij474s7L8'
    
    # Crear el servicio de YouTube
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    #sacamos el titulo del video y su creador
    titulo, canal = obtener_detalles_video(youtube, video_id)
    
    # Crear la ruta donde guardar
    canal_ajustado = canal.lower().replace(" ", "_").replace("/", "_")

    guardar = dir_cache / canal_ajustado
    guardar.mkdir(parents=True, exist_ok=True)  # Crear directorios del canal si no existen
    
    # Ruta del archivo HTML
    titulo_ajustado = titulo.lower().replace(" ", "_").replace("/", "_")

    archivo_json = guardar / (titulo_ajustado + ".json")
    
    # Verificar si el archivo ya existe
    if archivo_json.exists():
        print(f"El archivo de comentarios ya existe en {archivo_json}. No se generará de nuevo.")
        return
    
    # Obtener los comentarios del video
    print(f"Obteniendo comentarios de video {video_url}...")
    comentarios = obtener_comentarios(youtube, video_id)

    # Guardar los comentarios en un archivo JSON
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=4)
    
    print(f"Comentarios guardados en '{archivo_json}'.")

if __name__ == "__main__":
    dir_cache.mkdir(parents=True, exist_ok=True)
    video_url = input("Introduce la URL del video de YouTube: ")    
    video_id = extraer_video_id(video_url)
    sacar_comentarios(video_id)

