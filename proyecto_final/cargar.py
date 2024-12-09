from pathlib import Path

# Ruta al directorio de caché
dir_cache = Path("cache")

def listar_canales():
    """Lista todos los canales disponibles en el directorio de caché."""
    canales = sorted([d.name for d in dir_cache.iterdir() if d.is_dir()])
    if not canales:
        print("No se encontraron canales en la caché.")
        return []
    
    print("\nCanales disponibles:")
    for idx, canal in enumerate(canales):
        print(f"{idx + 1}. {canal}")
    return canales

def listar_videos(canal):
    """Lista todos los videos disponibles para un canal."""
    carpeta_canal = dir_cache / canal
    if not carpeta_canal.exists():
        print(f"La carpeta del canal {canal} no existe en el caché.")
        return []

    videos = sorted(carpeta_canal.glob("*.html"))
    if not videos:
        print(f"No se encontraron videos en la carpeta del canal {canal}.")
        return []
    
    print(f"\nVideos disponibles en el canal {canal}:")
    for idx, video in enumerate(videos):
        print(f"{idx + 1}. {video.stem}")  # .stem muestra el nombre del archivo sin extensión
    return videos

def cargar():
    # Listar canales
    canales = listar_canales()
    if not canales:
        return

    # Seleccionar un canal
    try:
        seleccion_canal = int(input("\nSelecciona un canal (número): ")) - 1
        if seleccion_canal < 0 or seleccion_canal >= len(canales):
            print("Selección no válida.")
            return
        canal = canales[seleccion_canal]
    except ValueError:
        print("Entrada no válida.")
        return

    # Listar videos del canal seleccionado
    videos = listar_videos(canal)
    if not videos:
        return

    # Seleccionar un video
    try:
        seleccion_video = int(input("\nSelecciona un video (número): ")) - 1
        if seleccion_video < 0 or seleccion_video >= len(videos):
            print("Selección no válida.")
            return
        video = videos[seleccion_video]
    except ValueError:
        print("Entrada no válida.")
        return

    # Cargar el video seleccionado
    datos = video.read_text(encoding="utf-8")
    
    return datos