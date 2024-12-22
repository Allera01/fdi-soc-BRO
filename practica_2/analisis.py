import click
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import os

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
def generate_graphics(posts, usuarios):
    # Frecuencia de palabras
    word_counts = posts["descripcion"].apply(preprocess_text).str.split().explode().value_counts().head(20)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=word_counts.values, y=word_counts.index, palette="viridis")
    plt.title("Top 20 palabras más frecuentes")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabras")
    plt.savefig("frecuencia_palabras.png")

    # Tendencia temporal de sentimientos
    posts["sentiment"] = posts["descripcion"].apply(lambda x: analyze_sentiment(preprocess_text(x))[0])
    posts["fecha"] = pd.to_datetime(posts["fecha"], errors='coerce')
    sentiment_trend = posts.groupby(posts["fecha"].dt.date)["sentiment"].mean()
    plt.figure(figsize=(10, 6))
    sentiment_trend.plot()
    plt.title("Tendencia del sentimiento a lo largo del tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Sentimiento promedio")
    plt.savefig("tendencia_sentimiento.png")

    # Usuarios más activos
    top_users = usuarios.sort_values(by="posts", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_users["posts"], y=top_users["nombre"], palette="coolwarm")
    plt.title("Top 10 Usuarios más Activos")
    plt.xlabel("Número de Posts")
    plt.ylabel("Usuario")
    plt.savefig("usuarios_activos.png")

# Generar informe Markdown
def generate_markdown():
    report_content = """# Informe de Análisis de Posts

## Introducción

El presente informe detalla los resultados del análisis realizado sobre un conjunto de datos extraído de los posts. El objetivo principal es identificar patrones, tendencias y relaciones entre el contenido, la actividad de los usuarios y las características textuales.

## Metodología

1. **Herramientas utilizadas:**
   - Python: para la manipulación y análisis de datos.
   - Pandas: para el manejo de los conjuntos de datos.
   - NLTK: para el procesamiento del lenguaje natural.
   - TextBlob: para el análisis de sentimientos.
   - Matplotlib y Seaborn: para la generación de gráficos.

2. **Preprocesamiento de datos:**
   - Los textos fueron limpiados para eliminar stopwords, convertir a minúsculas y tokenizar palabras.
   - Se analizó la polaridad y subjetividad de los textos para determinar el sentimiento.

3. **Análisis:**
   - Frecuencia de palabras.
   - Tendencias de sentimiento a lo largo del tiempo.
   - Actividad de los usuarios.

## Resultados

### Frecuencia de Palabras

![Frecuencia de palabras](frecuencia_palabras.png)

### Tendencia del Sentimiento

![Tendencia del sentimiento](tendencia_sentimiento.png)

### Usuarios más Activos

![Usuarios más activos](usuarios_activos.png)

## Conclusiones

- Los temas más mencionados reflejan intereses y preocupaciones predominantes de los usuarios.
- Las fluctuaciones en los sentimientos sugieren posibles relaciones con eventos externos o cambios en la dinámica de interacción en la plataforma.
- Los usuarios más activos tienen un impacto significativo en el contenido generado.

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
def main(posts, usuarios):
    # Cargar datos
    posts_df = pd.read_csv(posts)
    usuarios_df = pd.read_csv(usuarios)

    # Preprocesar y analizar
    generate_graphics(posts_df, usuarios_df)

    # Generar informe
    generate_markdown()

    print("Análisis completado. Informe generado en informe.md y gráficos en la carpeta principal del proyecto.")

if __name__ == "__main__":
    main()