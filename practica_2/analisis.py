import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import string
import seaborn as sns


# Cargar y filtrar datos
def load_and_filter_data(file_path, retweet_threshold=10, sample_size=1000):
    data = pd.read_csv(file_path)
    filtered_data = data[data["retweet_count"] >= retweet_threshold]
    sampled_data = (
        filtered_data.sample(n=sample_size, random_state=42)
        if len(filtered_data) > sample_size
        else filtered_data
    )
    return sampled_data


# Procesar texto
def preprocess_text(text, stopwords):
    tokens = text.lower().split()  # Dividir texto en palabras
    tokens = [word.strip(string.punctuation) for word in tokens]  # Quitar puntuación
    tokens = [
        word for word in tokens if word.isalnum() and word not in stopwords
    ]  # Filtrar
    return tokens


# Análisis de términos frecuentes
def analyze_frequent_terms(data, text_column, stopwords, top_n=10):
    data["tokens"] = data[text_column].apply(lambda x: preprocess_text(x, stopwords))
    all_tokens = [token for tokens in data["tokens"] for token in tokens]
    term_counts = Counter(all_tokens).most_common(top_n)
    return term_counts


# Guardar gráfico como PNG
def save_plot_as_png(filename):
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# Graficar términos frecuentes
def plot_frequent_terms(term_counts):
    terms, counts = zip(*term_counts)
    plt.figure(figsize=(10, 6))
    plt.bar(terms, counts, color="skyblue")
    plt.title("Términos más frecuentes en los tuits", fontsize=14)
    plt.xlabel("Términos", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    save_plot_as_png("frequent_terms.png")


# Relación entre retweets y longitud del texto
def analyze_retweets_vs_length(data):
    data["text_length"] = data["text"].apply(len)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="text_length", y="retweet_count", data=data, alpha=0.6)
    plt.title("Relación entre longitud del texto y retweets", fontsize=14)
    plt.xlabel("Longitud del texto", fontsize=12)
    plt.ylabel("Cantidad de retweets", fontsize=12)
    save_plot_as_png("retweets_vs_length.png")


# Análisis temporal de tuits
def analyze_tweets_over_time(data):
    data["created_at"] = pd.to_datetime(data["created_at"])
    data.set_index("created_at", inplace=True)
    tweets_over_time = data.resample("D").size()
    plt.figure(figsize=(10, 6))
    tweets_over_time.plot(color="orange")
    plt.title("Cantidad de tuits a lo largo del tiempo", fontsize=14)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Cantidad de tuits", fontsize=12)
    save_plot_as_png("tweets_over_time.png")


# Relación entre palabras clave y retweets
def analyze_keywords_vs_retweets(data, keywords):
    for keyword in keywords:
        data[keyword] = data["text"].str.contains(keyword, case=False, na=False)
    keyword_retweets = data.groupby(keywords)["retweet_count"].mean()

    # Usar valores booleanos para etiquetas del eje x
    keyword_labels = [str(comb) for comb in keyword_retweets.index]

    keyword_retweets.index = keyword_labels
    plt.figure(figsize=(10, 6))
    keyword_retweets.plot(kind="bar", color="purple")
    plt.title("Promedio de retweets según palabras clave", fontsize=14)
    plt.xlabel("Palabras clave (cyberpunk, 2077, game, genshinimpact)", fontsize=12)
    plt.ylabel("Promedio de retweets", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    save_plot_as_png("keywords_vs_retweets.png")


# Distribución de retweets
def analyze_retweet_distribution(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data["retweet_count"], bins=30, kde=True, color="green")
    plt.title("Distribución de retweets", fontsize=14)
    plt.xlabel("Cantidad de retweets", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    save_plot_as_png("retweet_distribution.png")


# Sustituir caracteres Unicode
UNICODE_REPLACEMENTS = {
    "原": "\\textbackslash{}u539F",
    "神": "\\textbackslash{}u795E",
    # Agregar más caracteres si es necesario
}


def replace_unicode(text):
    for char, replacement in UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    return text


def diagrama_circular_dispositivos(df):

    device_counts = df["source"].value_counts()

    # Calcular el umbral del 1% sobre el total de tuits
    total_tweets = device_counts.sum()
    threshold = total_tweets * 0.015

    # Crear una nueva serie para almacenar los dispositivos agrupados
    device_counts_grouped = device_counts[device_counts >= threshold]
    device_counts_grouped["Otros"] = device_counts[device_counts < threshold].sum()

    # Crear el gráfico circular
    plt.figure(figsize=(8, 8))
    device_counts_grouped.plot(
        kind="pie", autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors
    )
    plt.title("Distribución de tuits por dispositivo (agrupados los menores al 1.5%)")
    plt.ylabel("")  # Ocultar la etiqueta del eje y
    plt.savefig("dispositivos.png")


def sacar_tuits_horas(bf):
    # Convierte la columna ’created_at’ a tipo datetime
    bf["created_at"] = pd.to_datetime(bf["created_at"])
    # Extrae la hora
    bf["hora"] = bf["created_at"].dt.hour
    # Cuenta la cantidad de tweets por hora
    tweets_por_hora = bf["hora"].value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    plt.bar(tweets_por_hora.index, tweets_por_hora.values, color="skyblue")
    plt.xlabel("Hora del día")
    plt.ylabel("Cantidad de tweets")
    plt.title("Cantidad de tweets por hora")
    plt.xticks(tweets_por_hora.index)  # Asegúrate de que todas las horas se muestren
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig("horas.png")


# Crear informe en Markdown
def create_markdown_report(file_path, term_counts, output_path, additional_analyses):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Práctica 2: Análisis de tuits sobre Cyberpunk\n\n")
        f.write(
            f"**Autores:** Mario Carrilero Sánchez, Mario Gallego Hernández, Diego Linares Espíldora, Álvaro Llera Calderón\n\n"
        )
        f.write(f"## Archivo Analizado\n\n")
        f.write(f"**Ruta del archivo**: {file_path}\n\n")
        f.write(f"## Procedimiento\n\n")
        f.write(
            "1. Cargamos los datos desde uno de los archivos CSV (cyberpunk.csv) proporcionados por el profesor desde el Campus Virtual.\n"
            "2. Filtramos los tuits con al menos 10 retweets para enfocarnos en los de mayor relevancia.\n"
            "3. Seleccionamos una muestra representativa de hasta 1000 registros.\n"
            "4. Procesamos el contenido textual eliminando puntuación, convirtiendo a minúsculas y eliminando stopwords.\n"
            "5. Analizamos los términos más frecuentes para identificar patrones en el contenido.\n"
            "6. Exploramos las relaciones clave mediante gráficos, como la longitud del texto y los retweets, tendencias temporales, palabras clave y la distribución de retweets.\n"
        )

        f.write(f"\n## Términos Más Frecuentes\n\n")
        f.write("| Término | Frecuencia |\n")
        f.write("|---------|------------|\n")
        for term, count in term_counts:
            term = replace_unicode(term)
            f.write(f"| {term} | {count} |\n")
        f.write(f"\n![Términos más frecuentes en los tuits](frequent_terms.png)\n\n")

        f.write(f"\n## Análisis Adicionales\n\n")
        for analysis, image_file in additional_analyses:
            f.write(f"### {analysis}\n\n")
            if analysis == "Relación entre longitud del texto y retweets":
                f.write(
                    "Este gráfico muestra cómo la longitud de un tuit afecta a su popularidad, medida en retweets.\n"
                )
            elif analysis == "Cantidad de tuits a lo largo del tiempo":
                f.write(
                    "Este gráfico refleja la distribución temporal de los tuits, destacando picos de actividad.\n"
                )
            elif analysis == "Distribucion de tweets por horas":
                f.write(
                    "Este grafico muestra las horas en las que más se han publicado tweets.\n"
                )
            elif analysis == "Promedio de retweets según palabras clave":
                f.write(
                    "Aquí se comparan las palabras clave más relevantes según su influencia en los retweets.\n"
                )
            elif analysis == "Distribución de retweets":
                f.write(
                    "Este gráfico ilustra cómo están distribuidos los retweets en el conjunto de datos.\n"
                )
            elif analysis == "Dispositivos donde se realizan los tweets":
                f.write(
                    "En este grafico analizamos los dispositivos en los que más se twiteó, habiendo un gran reparto entre la propia aplicación de Twiter, iPhone y Android, siendo la que más en la aplicación de twiter, pero sin sacar gran ventaja a las otras dos. Cabe destacar que este análisis los hicimos con un gráfico circular.\n"
                )
            f.write(f"\n![{analysis}]({image_file})\n\n")
