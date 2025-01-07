import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import Counter
import string
from textblob import TextBlob
from extract import extract_comments_from_json
import seaborn as sns

def procesar_texto(texto, palabras_vacias):
    """
    Procesa el texto eliminando puntuación, convirtiendo a minúsculas y filtrando palabras vacías.
    """
    tokens = texto.lower().split()
    tokens = [palabra.strip(string.punctuation) for palabra in tokens]
    tokens = [palabra for palabra in tokens if palabra.isalnum() and palabra not in palabras_vacias]
    return tokens

def analizar_terminos_frecuentes(comentarios, palabras_vacias, top_n=10):
    """
    Analiza los términos más frecuentes en los comentarios.
    """
    tokens = [
        token
        for comentario in comentarios
        for token in procesar_texto(comentario["text"], palabras_vacias)
    ]
    conteo_terminos = Counter(tokens).most_common(top_n)
    return conteo_terminos

def graficar_terminos_frecuentes(conteo_terminos):
    """
    Genera un gráfico de los términos más frecuentes.
    """
    terminos, frecuencias = zip(*conteo_terminos)
    plt.figure(figsize=(10, 6))
    plt.bar(terminos, frecuencias, color="skyblue")
    plt.title("Términos más frecuentes en los comentarios", fontsize=14)
    plt.xlabel("Términos", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig("terminos_frecuentes.png")
    plt.close()

def analizar_distribucion_sentimientos(comentarios):
    """
    Analiza la distribución de la polaridad de los comentarios.
    """
    polaridades = [TextBlob(comentario["text"]).sentiment.polarity for comentario in comentarios]
    plt.figure(figsize=(10, 6))
    sns.histplot(polaridades, bins=30, kde=True, color="green")
    plt.title("Distribución de la polaridad", fontsize=14)
    plt.xlabel("Polaridad", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.tight_layout()
    plt.savefig("distribucion_polaridad.png")
    plt.close()

def analizar_likes_vs_longitud(comentarios):
    """
    Analiza la relación entre la longitud de los comentarios y los likes.
    """
    longitudes_texto = [len(comentario["text"]) for comentario in comentarios]
    likes = [comentario["like_count"] for comentario in comentarios]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=longitudes_texto, y=likes, alpha=0.6)
    plt.title("Relación entre longitud del comentario y likes", fontsize=14)
    plt.xlabel("Longitud del comentario", fontsize=12)
    plt.ylabel("Likes", fontsize=12)
    plt.tight_layout()
    plt.savefig("longitud_vs_likes.png")
    plt.close()

def analizar_comentarios_tiempo(comentarios):
    """
    Analiza la cantidad de comentarios a lo largo del tiempo.
    """
    fechas = [datetime.strptime(comentario["published_at"], "%Y-%m-%dT%H:%M:%SZ") for comentario in comentarios]
    fechas_ordenadas = sorted(fechas)
    conteo_diario = Counter(fecha.date() for fecha in fechas_ordenadas)
    dias, cantidades = zip(*sorted(conteo_diario.items()))

    plt.figure(figsize=(10, 6))
    plt.plot(dias, cantidades, marker="o", linestyle="-", color="orange")
    plt.title("Cantidad de comentarios a lo largo del tiempo", fontsize=14)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Cantidad de comentarios", fontsize=12)
    plt.tight_layout()
    plt.savefig("comentarios_tiempo.png")
    plt.close()

def analizar_palabras_clave_likes(comentarios, palabras_clave):
    """
    Analiza la relación entre palabras clave específicas y la cantidad promedio de likes.
    """
    likes_palabras = {palabra: [] for palabra in palabras_clave}

    for comentario in comentarios:
        texto = comentario["text"].lower()
        for palabra in palabras_clave:
            if palabra in texto:
                likes_palabras[palabra].append(comentario["like_count"])

    likes_promedio = {
        palabra: (sum(likes) / len(likes)) if likes else 0
        for palabra, likes in likes_palabras.items()
    }

    palabras, promedios = zip(*likes_promedio.items())
    plt.figure(figsize=(10, 6))
    plt.bar(palabras, promedios, color="purple")
    plt.title("Promedio de likes según palabras clave", fontsize=14)
    plt.xlabel("Palabras clave", fontsize=12)
    plt.ylabel("Promedio de likes", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig("palabras_clave_vs_likes.png")
    plt.close()

def generar_graficos(archivo_json):
    """
    Genera gráficos basados en los comentarios extraídos de un archivo JSON de YouTube.
    """
    # Extraer los comentarios
    comentarios = extract_comments_from_json(archivo_json)

    if not comentarios:
        print("No se encontraron comentarios con datos de likes.")
        return

    # --- Análisis de términos más frecuentes ---
    palabras_vacias = {
        "el", "la", "los", "las", "un", "unos", "una", "unas",
        "y", "o", "u", "de", "del", "al", "a",
        "en", "por", "para", "con", "sin", "sobre", "entre", "hacia",
        "que", "qué", "como", "cómo", "cuando", "cuándo", "donde", "dónde",
        "es", "son", "fue", "fueron", "será", "serán", "está", "están", "estaba", "estaban",
        "se", "lo", "le", "les", "nos", "me", "te", "mi", "tu", "su",
        "él", "ella", "ellos", "ellas", "esto", "eso", "aquello",
        "sí", "no", "también", "tan", "tanto", "muy",
        "pero", "aunque", "porque", "pues",
        "ya", "aún", "todavía", "más", "menos", "mucho", "poco",
        "ni", "si", "e", "además", "mientras",
        "ahora", "entonces", "luego", "después",
        "antes", "durante", "siempre", "nunca", "casi", "pronto", "tarde",
        "vez", "veces", "algún", "ningún", "todo", "todos", "toda", "todas",
        "otro", "otros", "otra", "otras", "cualquier", "cualquiera",
        "quien", "quienes", "cuyo", "cuya", "cuyos", "cuyas",
        "algo", "alguien", "nada", "nadie",
        "qué", "quién", "cómo", "cuándo", "dónde",
        "hoy", "ayer", "mañana", "aquí", "allí", "allá", "acá",
        "dos", "tres", "varios", "muchos", "algunos", "pocos",
        "mi", "mis", "tu", "tus", "su", "sus", "nuestro", "nuestra", "nuestros", "nuestras",
        "vuestra", "vuestro", "vuestros", "vuestras"
    }
    conteo_terminos = analizar_terminos_frecuentes(comentarios, palabras_vacias)
    graficar_terminos_frecuentes(conteo_terminos)
    print("Gráfico de términos frecuentes generado: 'terminos_frecuentes.png'.")

    # --- Distribución de la polaridad ---
    analizar_distribucion_sentimientos(comentarios)
    print("Gráfico de distribución de polaridad generado: 'distribucion_polaridad.png'.")

    # --- Relación entre longitud del texto y likes ---
    analizar_likes_vs_longitud(comentarios)
    print("Gráfico de longitud vs likes generado: 'longitud_vs_likes.png'.")

    # --- Análisis de comentarios a lo largo del tiempo ---
    analizar_comentarios_tiempo(comentarios)
    print("Gráfico de comentarios a lo largo del tiempo generado: 'comentarios_tiempo.png'.")

    # --- Análisis de palabras clave y likes ---
    palabras_clave = ["video", "bueno", "malo", "excelente"]
    analizar_palabras_clave_likes(comentarios, palabras_clave)
    print("Gráfico de palabras clave vs likes generado: 'palabras_clave_vs_likes.png'.")
