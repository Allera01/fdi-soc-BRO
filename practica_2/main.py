import click
from analisis import (
    load_and_filter_data,
    analyze_frequent_terms,
    plot_frequent_terms,
    analyze_retweets_vs_length,
    analyze_tweets_over_time,
    analyze_keywords_vs_retweets,
    analyze_retweet_distribution,
    create_markdown_report,
    diagrama_circular_dispositivos,
    sacar_tuits_horas,
)


@click.command(
    help="Este programa analiza propiedades de una red de grafos usando un archivo de lista de aristas.\n"
)  # Define el comando principal
@click.option(
    "-rvl",
    "--rt_vs_lenght",
    is_flag=True,
    help="Muestra la distribucion entre la cantidad de retweets y el numero de palabras.\n",
)
@click.option(
    "-tt",
    "--tweets_time",
    is_flag=True,
    help="Muestra una grafica donde se indica la cantidad de tweets que ha habido por dia.\n",
)
@click.option(
    "-wvr",
    "--words_vs_rt",
    is_flag=True,
    help="Muestra la cantidad de tweets que tienen ciertas palabras que hemos seleccionado.\n",
)
@click.option(
    "-disp",
    "--dispositivos",
    is_flag=True,
    help="Muestra una grafica donde vemos la distribucion de dispositivos.\n",
)
@click.option(
    "-rdis",
    "--rt_distribution",
    is_flag=True,
    help="Muestra una grafica que ilustra como estan distribuidos los retweets.\n",
)
@click.option(
    "-h",
    "--horas",
    is_flag=True,
    help="Muestra una grafica que ilustra como estan distribuidos los tweets por horas.\n",
)
@click.option(
    "-a", "--all", is_flag=True, help="Se ejecutan todas las funciones opcionales.\n"
)
def my_main(
    rt_vs_lenght, tweets_time, words_vs_rt, dispositivos, rt_distribution, horas, all
):
    # Ruta del archivo CSV
    file_path = "cyberpunk.csv"
    output_markdown = "informe.md"

    # Stopwords predefinidas
    stopwords = {
        "i",
        "me",
        "my",
        "myself",
        "we",
        "our",
        "ours",
        "ourselves",
        "you",
        "your",
        "yours",
        "yourself",
        "he",
        "him",
        "his",
        "himself",
        "she",
        "her",
        "hers",
        "herself",
        "it",
        "its",
        "itself",
        "they",
        "them",
        "their",
        "theirs",
        "themselves",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "these",
        "those",
        "am",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "having",
        "do",
        "does",
        "did",
        "doing",
        "a",
        "an",
        "the",
        "and",
        "but",
        "if",
        "or",
        "because",
        "as",
        "until",
        "while",
        "of",
        "at",
        "by",
        "for",
        "with",
        "about",
        "against",
        "between",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "to",
        "from",
        "up",
        "down",
        "in",
        "out",
        "on",
        "off",
        "over",
        "under",
        "again",
        "further",
        "then",
        "once",
        "here",
        "there",
        "when",
        "where",
        "why",
        "how",
        "all",
        "any",
        "both",
        "each",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
        "s",
        "t",
        "can",
        "will",
        "just",
        "don",
        "should",
        "now",
    }

    # Cargar y procesar datos
    data = load_and_filter_data(file_path)
    if horas or all:
        sacar_tuits_horas(data)

    # Analizar términos frecuentes
    term_counts = analyze_frequent_terms(data, "text", stopwords)

    # Graficar términos frecuentes
    plot_frequent_terms(term_counts)

    # Analizar relaciones adicionales
    if rt_vs_lenght or all:
        analyze_retweets_vs_length(data)
    if tweets_time or all:
        analyze_tweets_over_time(data)

    if words_vs_rt or all:
        analyze_keywords_vs_retweets(
            data, ["cyberpunk", "2077", "game", "genshinimpact"]
        )
    if rt_distribution or all:
        analyze_retweet_distribution(data)
    if dispositivos or all:
        diagrama_circular_dispositivos(data)
    # Generar informe en Markdown
    additional_analyses = [
        ("Relación entre longitud del texto y retweets", "retweets_vs_length.png"),
        ("Cantidad de tuits a lo largo del tiempo", "tweets_over_time.png"),
        ("Promedio de retweets según palabras clave", "keywords_vs_retweets.png"),
        ("Distribución de retweets", "retweet_distribution.png"),
        ("Dispositivos donde se realizan los tweets", "dispositivos.png"),
        ("Distribucion de tweets por horas", "horas.png"),
    ]
    create_markdown_report(file_path, term_counts, output_markdown, additional_analyses)

    print(f"Informe generado: {output_markdown}")


if __name__ == "__main__":
    my_main()