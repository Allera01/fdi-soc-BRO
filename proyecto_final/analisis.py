import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from textblob import TextBlob
from extract import extract_comments_from_json

def obtener_polaridad(texto):
    """
    Devuelve la polaridad de un comentario usando TextBlob.
    """
    blob = TextBlob(texto)
    return blob.sentiment.polarity  # Devuelve un valor entre -1 y 1


def generar_graficos(archivo_json):
    """
    Genera gráficos basados en los comentarios extraídos de un archivo JSON de YouTube.
    """

    # Extraer los comentarios
    comments = extract_comments_from_json(archivo_json)

    if not comments:
        print("No se encontraron comentarios con datos de likes.")
        return

    # Obtener datos para el gráfico de likes
    likes = [comment['like_count'] for comment in comments]
    comentarios = [comment['text'][:40] for comment in comments]  # Limitar el texto de los comentarios a 40 caracteres

    # Obtener datos para el gráfico de respuestas (por ahora no hay respuesta en el JSON proporcionado)
    respuestas = [0 for comment in comments]  # Poner 0 como predeterminado si no hay respuestas en este ejemplo

    # Obtener polaridad y likes
    polaridades = [obtener_polaridad(comment['text']) for comment in comments]
    likes = [comment['like_count'] for comment in comments]
    comentarios = [comment['text'][:40] for comment in comments]  # Limitar el texto de los comentarios a 40 caracteres

    #--- Crear gráfico de polaridad vs likes ---
    plt.figure(figsize=(10, 6))
    plt.scatter(polaridades, likes, color='purple', alpha=0.6)

    # Etiquetas y título
    plt.xlabel('Polaridad del Sentimiento')
    plt.ylabel('Likes')
    plt.title('Polaridad vs Likes en los Comentarios')

    # Ajustes en los ejes
    plt.xlim(-1, 1)  # Rango de la polaridad
    plt.ylim(0, max(likes) + 10)  # Ajuste dinámico para los likes

    plt.tight_layout()
    plt.savefig('grafico_polaridad_vs_likes.png')
    plt.close()

    print("Gráfico generado y guardado como 'grafico_polaridad_vs_likes.png'.")

    #--- Grafico de sentimientos entre sentimiento del comenatario frente a la cantidad de respuestas ---
    # Inicializar contadores de respuestas para comentarios positivos y negativos
    respuestas_positivas = 0
    respuestas_negativas = 0

    # Recorrer los comentarios para contar respuestas
    for comment in comments:
        polaridad = obtener_polaridad(comment['text'])
        if polaridad >= 0:
            respuestas_positivas += len(comment['replies'])
        else:
            respuestas_negativas += len(comment['replies'])

    # Crear gráfico de barras
    labels = ['Comentarios Positivos', 'Comentarios Negativos']
    data = [respuestas_positivas, respuestas_negativas]

    # Crear gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(labels, data, color=['green', 'red'])

    # Etiquetas y título
    plt.xlabel('Tipo de Sentimiento')
    plt.ylabel('Número de Respuestas')
    plt.title('Respuestas en Comentarios Positivos vs Negativos')

    # Mostrar el gráfico
    plt.tight_layout()
    plt.savefig('grafico_respuestas_sentimiento.png')
    plt.close()

    print("Gráfico generado y guardado como 'grafico_respuestas_sentimiento.png'.")

    #--- Gráfico Likes vs Fecha de Publicación ---
    # Convertir la fecha de publicación a formato datetime
    fechas = [datetime.strptime(comment['published_at'], '%Y-%m-%dT%H:%M:%SZ') for comment in comments]
    
    # Ordenar los comentarios por fecha
    sorted_comments = sorted(zip(fechas, likes), key=lambda x: x[0])

    # Desempaquetar los comentarios ordenados
    sorted_fechas, sorted_likes = zip(*sorted_comments)

    # Crear el gráfico de Likes vs Fecha de Publicación
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_fechas, sorted_likes, marker='o', linestyle='-', color='b')
    
    # Formatear las fechas en el eje X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))  # Cada 10 días
    plt.gcf().autofmt_xdate()  # Rotar las fechas para que se vean bien

    plt.xlabel('Fecha de Publicación')
    plt.ylabel('Número de Likes')
    plt.title('Likes en función de la Fecha de Publicación')
    plt.tight_layout()

    # Guardar el gráfico
    plt.savefig('grafico_likes_vs_fecha.png')
    print("Gráfico generado y guardado como 'grafico_likes_vs_fecha.png'.")
    plt.close()


def filtrar_y_analizar_palabra_video(data):
    """Filtra los comentarios que contienen la palabra 'video' y analiza su polaridad."""
    fechas_polaridad = []
    # Extraer los comentarios
    comentarios = extract_comments_from_json(data)

    for comentario in comentarios:
        if 'snippet' in comentario and 'topLevelComment' in comentario['snippet']:
            snippet = comentario['snippet']['topLevelComment']['snippet']
            texto = snippet['textDisplay']
            fecha = snippet['publishedAt']
                
            # Verificar si el texto contiene la palabra 'video'
            if 'malo' in texto.lower():
                polaridad = obtener_polaridad(texto)
                fechas_polaridad.append((fecha, polaridad))
    
    return fechas_polaridad

def graficar_evolucion_palabra_video(fechas_polaridad):
    """Genera un gráfico que muestra la evolución de la polaridad de la palabra 'video' en comentarios."""
    # Convertir fechas a formato datetime
    fechas_polaridad = [(datetime.fromisoformat(fecha[:-1]), polaridad) for fecha, polaridad in fechas_polaridad]
    
    # Ordenar por fecha
    fechas_polaridad.sort(key=lambda x: x[0])
    
    # Agrupar por día y calcular polaridad promedio
    polaridad_por_dia = {}
    for fecha, polaridad in fechas_polaridad:
        dia = fecha.date()
        if dia not in polaridad_por_dia:
            polaridad_por_dia[dia] = []
        polaridad_por_dia[dia].append(polaridad)

    dias = sorted(polaridad_por_dia.keys())
    polaridades_promedio = [sum(polaridad_por_dia[dia]) / len(polaridad_por_dia[dia]) for dia in dias]

    # Graficar la evolución
    plt.figure(figsize=(10, 6))
    plt.plot(dias, polaridades_promedio, marker='o', color='blue', label='Polaridad Promedio')
    plt.axhline(0, color='red', linestyle='--', label='Neutral')
    plt.title("Evolución de la polaridad de la palabra 'video' en comentarios")
    plt.xlabel("Fecha")
    plt.ylabel("Polaridad Promedio")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('evolucion_palabra_video.png')
    print("Gráfico generado y guardado como 'evolucion_palabra_video.png'.")
    plt.close()