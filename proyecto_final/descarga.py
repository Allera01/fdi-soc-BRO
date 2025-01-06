import googleapiclient.discovery
import json
import re
from pathlib import Path

dir_cache = Path("cache")

# Función para obtener los comentarios de un video
def obtener_comentarios(youtube, video_id):
    comentarios = []
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100  # Puedes ajustar el número máximo de comentarios por página
    )
    
    while request:
        response = request.execute()
        comentarios.append(response)
        request = youtube.commentThreads().list_next(request, response)
    
    return comentarios

def extraer_video_id(url):
    regex = r"(?:https?://(?:www\.)?youtube\.com/.*[?&]v=|https?://youtu\.be/|https?://m\.youtube\.com/v/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("No se pudo extraer el ID del video de la URL.")

def obtener_detalles_video(youtube, video_id):
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
    api_key = 'AIzaSyAKa2JQhSNHvmzjqa1zr99niVij474s7L8'
    
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    # Obtener el título y canal del video
    titulo, canal = obtener_detalles_video(youtube, video_id)
    
    # Crear la ruta donde guardar
    canal_ajustado = canal.lower().replace(" ", "_").replace("/", "_")
    guardar = dir_cache / canal_ajustado
    guardar.mkdir(parents=True, exist_ok=True)
    
    # Ruta del archivo JSON
    titulo_ajustado = titulo.lower().replace(" ", "_").replace("/", "_")
    archivo_json = guardar / (titulo_ajustado + ".json")
    
    # Verificar si el archivo ya existe
    if archivo_json.exists():
        print(f"El archivo de comentarios ya existe en {archivo_json}. No se generará de nuevo.")
        return
    
    print(f"Obteniendo comentarios de video {video_id}...")
    comentarios = obtener_comentarios(youtube, video_id)
    
    # Guardar los comentarios en un archivo JSON
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=4)
    
    print(f"Comentarios guardados en '{archivo_json}'.")

def descargar():
    dir_cache.mkdir(parents=True, exist_ok=True)
    video_url = input("Introduce la URL del video de YouTube: ")    
    video_id = extraer_video_id(video_url)
    sacar_comentarios(video_id)








