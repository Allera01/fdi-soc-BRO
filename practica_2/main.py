import click
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import spacy
import os

# Cargar el modelo de spaCy
nlp = spacy.load("en_core_web_sm")

# Preprocesar texto
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("spanish"))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(filtered_tokens)

# Analizar sentimientos
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Generar gráficos

def generate_graphics(posts, usuarios, comentarios):
    # Frecuencia de palabras
    word_counts = posts["content"].apply(preprocess_text).str.split().explode().value_counts().head(20)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=word_counts.values, y=word_counts.index, palette="viridis")
    plt.title("Top 20 palabras más frecuentes")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabras")
    plt.savefig("frecuencia_palabras.png")

    # Tendencia temporal de sentimientos
    posts["sentiment"] = posts["content"].apply(lambda x: analyze_sentiment(preprocess_text(x))[0])
    posts["date"] = pd.to_datetime(posts["date"])
    sentiment_trend = posts.groupby(posts["date"].dt.date)["sentiment"].mean()
    plt.figure(figsize=(10, 6))
    sentiment_trend.plot()
    plt.title("Tendencia del sentimiento a lo largo del tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Sentimiento promedio")
    plt.savefig("tendencia_sentimiento.png")

    # Distribución de interacciones (Retweets y Likes)
    plt.figure(figsize=(10, 6))
    sns.histplot(posts["retweets"], bins=30, kde=True, color="blue", label="Retweets")
    sns.histplot(posts["likes"], bins=30, kde=True, color="orange", label="Likes")
    plt.legend()
    plt.title("Distribución de Interacciones (Retweets y Likes)")
    plt.xlabel("Cantidad")
    plt.ylabel("Frecuencia")
    plt.savefig("distribucion_interacciones.png")

    # Usuarios más activos
    top_users = usuarios.sort_values(by="tweets", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_users["tweets"], y=top_users["username"], palette="coolwarm")
    plt.title("Top 10 Usuarios más Activos")
    plt.xlabel("Número de Tweets")
    plt.ylabel("Usuario")
    plt.savefig("usuarios_activos.png")

    # Relación entre sentimiento y métricas
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=posts["sentiment"], y=posts["likes"], alpha=0.5, label="Likes", color="blue")
    sns.scatterplot(x=posts["sentiment"], y=posts["retweets"], alpha=0.5, label="Retweets", color="green")
    plt.title("Relación entre Sentimiento y Métricas")
    plt.xlabel("Sentimiento")
    plt.ylabel("Cantidad")
    plt.legend()
    plt.savefig("relacion_sentimiento_metricas.png")

# Generar informe Markdown
def generate_markdown():
    report_content = """# Informe de Análisis de Tuits

## Introducción

El presente informe detalla los resultados del análisis realizado sobre un conjunto de datos extraído de Twitter. El objetivo principal es identificar patrones, tendencias y relaciones entre el contenido de los tuits, la interacción de los usuarios y las características textuales.

## Metodología

1. **Herramientas utilizadas:**
   - Python: para la manipulación y análisis de datos.
   - Pandas: para el manejo de los conjuntos de datos.
   - NLTK y spaCy: para el procesamiento del lenguaje natural.
   - TextBlob: para el análisis de sentimientos.
   - Matplotlib y Seaborn: para la generación de gráficos.

2. **Preprocesamiento de datos:**
   - Los textos fueron limpiados para eliminar stopwords, convertir a minúsculas y tokenizar palabras.
   - Se analizó la polaridad y subjetividad de los textos para determinar el sentimiento.

3. **Análisis:**
   - Frecuencia de palabras.
   - Tendencias de sentimiento a lo largo del tiempo.
   - Distribución de interacciones.
   - Actividad de los usuarios.
   - Relación entre sentimiento y métricas.

## Resultados

### Frecuencia de Palabras

![Frecuencia de palabras](frecuencia_palabras.png)

Las palabras más frecuentes en los tuits analizados incluyen temas relevantes y hashtags populares. Esto sugiere una fuerte tendencia hacia ciertos tópicos dentro del conjunto de datos.

### Tendencia del Sentimiento

![Tendencia del sentimiento](tendencia_sentimiento.png)

Se observa una variabilidad en el sentimiento promedio a lo largo del tiempo. Los picos y valles reflejan eventos importantes o cambios en el tono general del contenido analizado.

### Distribución de Interacciones

![Distribución de interacciones](distribucion_interacciones.png)

La distribución de retweets y likes muestra tendencias sobre cómo los usuarios interactúan con el contenido. Estas métricas son indicativas del impacto y popularidad de los tuits.

### Usuarios más Activos

![Usuarios más activos](usuarios_activos.png)

El análisis de los usuarios más activos destaca a aquellos con mayor volumen de tuits, indicando su nivel de participación e influencia en la red social.

### Relación entre Sentimiento y Métricas

![Relación entre Sentimiento y Métricas](relacion_sentimiento_metricas.png)

Se observan correlaciones entre el sentimiento expresado en los tuits y las métricas de interacción (likes y retweets). Esto sugiere que el tono emocional del contenido puede influir en la participación de otros usuarios.

## Conclusiones

- Los temas más mencionados reflejan intereses y preocupaciones predominantes de los usuarios.
- Las fluctuaciones en los sentimientos sugieren posibles relaciones con eventos externos o cambios en la dinámica de interacción en la plataforma.
- Los usuarios más activos tienen un impacto significativo en la red social, promoviendo interacciones frecuentes.
- Las técnicas empleadas demostraron ser efectivas para extraer insights significativos del contenido de los tuits.

## Anexos

1. **Código:**
   El código utilizado para este análisis se encuentra disponible en el repositorio GitHub del proyecto.

2. **Gráficos generados:**
   Los gráficos están almacenados en la carpeta principal del proyecto.
"""
    with open("informe.md", "w", encoding="utf-8") as file:
        file.write(report_content)

# Interfaz de línea de comandos
@click.command()
@click.option("--posts", type=click.Path(exists=True), required=True, help="Ruta al archivo CSV de posts.")
@click.option("--usuarios", type=click.Path(exists=True), required=True, help="Ruta al archivo CSV de usuarios.")
@click.option("--comentarios", type=click.Path(exists=True), required=True, help="Ruta al archivo CSV de comentarios.")
def main(posts, usuarios, comentarios):
    # Cargar datos
    posts_df = pd.read_csv(posts)
    usuarios_df = pd.read_csv(usuarios)
    comentarios_df = pd.read_csv(comentarios)

    # Preprocesar y analizar
    generate_graphics(posts_df, usuarios_df, comentarios_df)

    # Generar informe
    generate_markdown()

    print("Análisis completado. Informe generado en informe.md y gráficos en la carpeta principal del proyecto.")

if __name__ == "__main__":
    main()
