import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import Counter
import string
from textblob import TextBlob
from extract import extract_comments_from_json
import seaborn as sns

def preprocess_text(text, stopwords):
    """
    Procesa el texto eliminando puntuación, convirtiendo a minúsculas y filtrando stopwords.
    """
    tokens = text.lower().split()
    tokens = [word.strip(string.punctuation) for word in tokens]
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords]
    return tokens


def analyze_frequent_terms(comments, stopwords, top_n=10):
    """
    Analiza los términos más frecuentes en los comentarios.
    """
    tokens = [
        token
        for comment in comments
        for token in preprocess_text(comment["text"], stopwords)
    ]
    term_counts = Counter(tokens).most_common(top_n)
    return term_counts


def plot_frequent_terms(term_counts):
    """
    Genera un gráfico de los términos más frecuentes.
    """
    terms, counts = zip(*term_counts)
    plt.figure(figsize=(10, 6))
    plt.bar(terms, counts, color="skyblue")
    plt.title("Términos más frecuentes en los comentarios", fontsize=14)
    plt.xlabel("Términos", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig("frequent_terms.png")
    plt.close()


def analyze_sentiment_distribution(comments):
    """
    Analiza la distribución de la polaridad de los comentarios.
    """
    polarities = [TextBlob(comment["text"]).sentiment.polarity for comment in comments]
    plt.figure(figsize=(10, 6))
    sns.histplot(polarities, bins=30, kde=True, color="green")
    plt.title("Distribución de la polaridad", fontsize=14)
    plt.xlabel("Polaridad", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.tight_layout()
    plt.savefig("sentiment_distribution.png")
    plt.close()


def analyze_likes_vs_length(comments):
    """
    Analiza la relación entre la longitud de los comentarios y los likes.
    """
    text_lengths = [len(comment["text"]) for comment in comments]
    likes = [comment["like_count"] for comment in comments]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=text_lengths, y=likes, alpha=0.6)
    plt.title("Relación entre longitud del comentario y likes", fontsize=14)
    plt.xlabel("Longitud del comentario", fontsize=12)
    plt.ylabel("Likes", fontsize=12)
    plt.tight_layout()
    plt.savefig("likes_vs_length.png")
    plt.close()


def analyze_comments_over_time(comments):
    """
    Analiza la cantidad de comentarios a lo largo del tiempo.
    """
    dates = [datetime.strptime(comment["published_at"], "%Y-%m-%dT%H:%M:%SZ") for comment in comments]
    sorted_dates = sorted(dates)
    daily_counts = Counter(date.date() for date in sorted_dates)
    days, counts = zip(*sorted(daily_counts.items()))

    plt.figure(figsize=(10, 6))
    plt.plot(days, counts, marker="o", linestyle="-", color="orange")
    plt.title("Cantidad de comentarios a lo largo del tiempo", fontsize=14)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Cantidad de comentarios", fontsize=12)
    plt.tight_layout()
    plt.savefig("comments_over_time.png")
    plt.close()

def analyze_keywords_vs_likes(comments, keywords):
    """
    Analiza la relación entre palabras clave específicas y la cantidad promedio de likes.
    """
    keyword_likes = {keyword: [] for keyword in keywords}

    for comment in comments:
        text = comment["text"].lower()
        for keyword in keywords:
            if keyword in text:
                keyword_likes[keyword].append(comment["like_count"])

    avg_likes = {
        keyword: (sum(likes) / len(likes)) if likes else 0
        for keyword, likes in keyword_likes.items()
    }

    keywords, averages = zip(*avg_likes.items())
    plt.figure(figsize=(10, 6))
    plt.bar(keywords, averages, color="purple")
    plt.title("Promedio de likes según palabras clave", fontsize=14)
    plt.xlabel("Palabras clave", fontsize=12)
    plt.ylabel("Promedio de likes", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig("keywords_vs_likes.png")
    plt.close()

def generar_graficos(archivo_json):
    """
    Genera gráficos basados en los comentarios extraídos de un archivo JSON de YouTube.
    """
    # Extraer los comentarios
    comments = extract_comments_from_json(archivo_json)

    if not comments:
        print("No se encontraron comentarios con datos de likes.")
        return

    # --- Análisis de términos más frecuentes ---
    stopwords = {"el", "la", "y", "de", "que", "a", "en", "un", "es", "se"}
    term_counts = analyze_frequent_terms(comments, stopwords)
    plot_frequent_terms(term_counts)
    print("Gráfico de términos frecuentes generado: 'frequent_terms.png'.")

    # --- Distribución de la polaridad ---
    analyze_sentiment_distribution(comments)
    print("Gráfico de distribución de polaridad generado: 'sentiment_distribution.png'.")

    # --- Relación entre longitud del texto y likes ---
    analyze_likes_vs_length(comments)
    print("Gráfico de longitud vs likes generado: 'likes_vs_length.png'.")

    # --- Análisis de comentarios a lo largo del tiempo ---
    analyze_comments_over_time(comments)
    print("Gráfico de comentarios a lo largo del tiempo generado: 'comments_over_time.png'.")

    # --- Análisis de palabras clave y likes ---
    keywords = ["video", "bueno", "malo", "excelente"]
    analyze_keywords_vs_likes(comments, keywords)
    print("Gráfico de palabras clave vs likes generado: 'keywords_vs_likes.png'.")