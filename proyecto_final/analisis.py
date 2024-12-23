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
    try:
        with open(archivo_json, 'r', encoding='utf-8') as file:
            comments_data = json.load(file)
    except FileNotFoundError:
        print(f"El archivo {archivo_json}.json no se encuentra.")
        return

    # Extraer los comentarios
    comments = extract_comments_from_json(comments_data)

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

    # Crear gráfico de polaridad vs likes
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

    '''Grafico de sentimientos entre sentimiento del comenatario frente a la cantidad de respuestas'''

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

    # ---- Gráfico Likes vs Fecha de Publicación ----
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
    plt.close()

    print("Gráficos generados y guardados como 'grafico_likes_comentarios.png', 'grafico_respuestas_comentarios.png' y 'grafico_likes_vs_fecha.png'.")
