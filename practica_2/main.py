import pandas as pd
import nltk
import re
import os
import string
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk import ngrams
from collections import Counter

nltk.download("punkt_tab")


# Quitar las URL y los signos de puntuación
def remove_punctuation(text):
    url_pattern = r"http[s]?://\S+|www\.\S+"
    # Eliminar URLs del texto
    text_without_urls = re.sub(url_pattern, "", text)
    # Tokenizar el texto
    tokens = word_tokenize(text_without_urls)
    # Filtrar tokens para eliminar signos de puntuación
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    return tokens


def grafico_polaridad_2p(palabra1, palabra2, datos):
    if not os.path.isfile("./grafico_polaridad_" + palabra1 + "_" + palabra2 + ".png"):
        df = datos
        df["polarity"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

        # Calcular la longitud del tweet
        df["tweet_length"] = df["text"].apply(len)

        # Filtrar los tweets que contienen las palabras
        df["contains_palabra1"] = df["tokens"].apply(lambda tokens: palabra1 in tokens)
        df["contains_palabra2"] = df["tokens"].apply(lambda tokens: palabra2 in tokens)

        # Filtrar solo las filas con las palabras
        df_palabra1_palabra2 = df[(df["contains_palabra1"]) | (df["contains_palabra2"])]

        # Crear gráfico de polaridad vs longitud del tweet, diferenciando las palabras
        plt.figure(figsize=(10, 6))

        # Graficar tweets con la palabra1
        plt.scatter(
            df_palabra1_palabra2[df_palabra1_palabra2["contains_palabra1"]][
                "tweet_length"
            ],
            df_palabra1_palabra2[df_palabra1_palabra2["contains_palabra1"]]["polarity"],
            color="blue",
            label=palabra1,
            alpha=0.5,
        )

        # Graficar tweets con la palabra2
        plt.scatter(
            df_palabra1_palabra2[df_palabra1_palabra2["contains_palabra2"]][
                "tweet_length"
            ],
            df_palabra1_palabra2[df_palabra1_palabra2["contains_palabra2"]]["polarity"],
            color="red",
            label=palabra2,
            alpha=0.5,
        )

        # Personalización del gráfico
        plt.xlabel("Longitud del Tweet")
        plt.ylabel("Polaridad")
        plt.title(
            "Relación entre Polaridad y Longitud del Tweet para "
            + palabra1
            + " y "
            + palabra2
        )
        plt.legend()
        plt.grid(True)
        plt.savefig("grafico_polaridad_" + palabra1 + "_" + palabra2 + ".png")


def grafico_polaridad_1p(palabra, datos):
    if not os.path.isfile("./grafico_polaridad_" + palabra + ".png"):
        df = datos
        df["polarity"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

        # Calcular la longitud del tweet
        df["tweet_length"] = df["text"].apply(len)

        # Filtrar los tweets que contienen la palabra
        df["contains_palabra"] = df["tokens"].apply(lambda tokens: palabra in tokens)

        # Filtrar solo las filas con la palabra
        df_palabra = df[(df["contains_palabra"])]

        # Crear gráfico de polaridad vs longitud del tweet
        plt.figure(figsize=(10, 6))

        # Graficar tweets con palabra
        plt.scatter(
            df_palabra[df_palabra["contains_palabra"]]["tweet_length"],
            df_palabra[df_palabra["contains_palabra"]]["polarity"],
            color="green",
            label=palabra,
            alpha=0.5,
        )

        # Personalización del gráfico
        plt.xlabel("Longitud del Tweet")
        plt.ylabel("Polaridad")
        plt.title("Relación entre Polaridad y Longitud del Tweet para " + palabra)
        plt.legend()
        plt.grid(True)
        plt.savefig("grafico_polaridad_" + palabra + ".png")


def sacar_bi_tri_gramas(df):
    if not os.path.isfile("./bigramas_trigramas.txt"):
        bigramas = []
        trigramas = []

        for tokens in df["tokens"]:
            bigramas.extend(ngrams(tokens, 2))  # Generar bigramas
            trigramas.extend(ngrams(tokens, 3))  # Generar trigramas

        # Contar frecuencias de bigramas y trigramas
        bigramas_frecuentes = Counter(bigramas)
        trigramas_frecuentes = Counter(trigramas)

        with open("bigramas_trigramas.txt", "w", encoding="utf-8") as file:
            file.write("Bigramas más frecuentes:\n")
            for bigrama, frecuencia in bigramas_frecuentes.most_common():
                if frecuencia > 50:
                    file.write(f"{bigrama}: {frecuencia}\n")

            file.write("\nTrigramas más frecuentes:\n")
            for trigrama, frecuencia in trigramas_frecuentes.most_common():
                if frecuencia > 50:
                    file.write(f"{trigrama}: {frecuencia}\n")

        # Mostrar los 10 bigramas y trigramas más comunes
        # print("Bigramas más comunes:", bigramas_frecuentes.most_common(20))
        # print("Trigramas más comunes:", trigramas_frecuentes.most_common(20))


def diagrama_circular_dispositivos(df):
    if not os.path.isfile("./dispositivos.png"):
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
        plt.title(
            "Distribución de tuits por dispositivo (agrupados los menores al 1.5%)"
        )
        plt.ylabel("")  # Ocultar la etiqueta del eje y
        plt.savefig("dispositivos.png")


def sacar_tuits_horas(bf):
    if not os.path.isfile("./horas.png"):
        # Convierte la columna 'created_at' a tipo datetime
        df["created_at"] = pd.to_datetime(bf["created_at"])

        # Extrae la hora
        df["hora"] = df["created_at"].dt.hour

        # Cuenta la cantidad de tweets por hora
        tweets_por_hora = df["hora"].value_counts().sort_index()

        plt.figure(figsize=(10, 5))
        plt.bar(tweets_por_hora.index, tweets_por_hora.values, color="skyblue")
        plt.xlabel("Hora del día")
        plt.ylabel("Cantidad de tweets")
        plt.title("Cantidad de tweets por hora")
        plt.xticks(
            tweets_por_hora.index
        )  # Asegúrate de que todas las horas se muestren
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.savefig("horas.png")


df = pd.read_csv("cyberpunk.csv")
df["tokens"] = df["text"].apply(remove_punctuation)

# crea la lista de palabras junto a su numero de apariciones
if not os.path.isfile("./token_counts.txt"):
    # Añadir a all_tokens todos los tokens sin repetición
    all_tokens = [token for tokens_list in df["tokens"] for token in tokens_list]
    # Contar la cantidad de veces que aparece cada token
    token_counts = pd.Series(all_tokens).value_counts()

    with open("token_counts.txt", "w", encoding="utf-8") as f:
        f.write(token_counts.to_string())

# tuits que tienen la localizacion activa
if not os.path.isfile("./tweets_con_location.txt"):
    # Filtrar tweets donde la columna 'location' no es None
    tweets_con_location = df[df["location"].notna()]

    with open("tweets_con_location.txt", "w", encoding="utf-8") as f:
        f.write(tweets_con_location.to_string())


def detectar_tema(texto):
    if re.search(r"\b(#?genshinimpact)\b", texto, re.IGNORECASE):
        return "Genshin"
    elif re.search(r"\b(cyberpunk\s*2077)\b", texto, re.IGNORECASE):
        return "Cyberpunk"
    return None


# cantidad de tuits con la palabra cyberpunk y genshin
if not os.path.isfile("./cyberpunkvsgenshin.png"):
    # Aplicar la función a la columna 'text'
    x = df["text"].apply(detectar_tema)

    # Contar la frecuencia de cada tema
    temas_count = x.value_counts()

    plt.figure(figsize=(8, 5))
    temas_count.plot(kind="bar", color=["blue", "orange"])
    plt.title("Menciones de los temas Cyberpunk y Genshin en Twitter")
    plt.xlabel("Tema")
    plt.ylabel("Cantidad de Menciones")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig("cyberpunkvsgenshin.png")

# Obtener los 100 usuarios con más tweets sin bots
if not os.path.isfile("./UsersSinBots.png"):
    filtered_df = df[df["user"] != df["source"]]
    user_tweet_counts = filtered_df["user"].value_counts()
    top_users = user_tweet_counts.head(10)
    plt.figure(figsize=(10, 8))
    plt.pie(
        top_users,
        labels=top_users.index,
        autopct=lambda p: f"{int(p * sum(top_users) / 100)}",
        startangle=140,
    )
    plt.title("Top 10 Usuarios por Cantidad de Tweets (Excluyendo bots)")
    plt.savefig("UsersSinBots.png")

# Obtener los 100 usuarios con más tweets con bots
if not os.path.isfile("./UsersBots.png"):
    user_tweet_count = df["user"].value_counts()
    top_user = user_tweet_count.head(10)
    plt.figure(figsize=(10, 8))
    plt.pie(
        top_user,
        labels=top_user.index,
        autopct=lambda p: f"{int(p * sum(top_user) / 100)}",
        startangle=140,
    )
    plt.title("Top 10 Usuarios por Cantidad de Tweets (Con bots)")
    plt.savefig("UsersBots.png")

grafico_polaridad_1p("cyberpunk", df)
grafico_polaridad_2p("good", "bad", df)
grafico_polaridad_2p("steam", "playstation", df)
grafico_polaridad_2p("patch", "bugs", df)
grafico_polaridad_2p("graphics", "performance", df)
grafico_polaridad_2p("story", "gameplay", df)
sacar_bi_tri_gramas(df)
diagrama_circular_dispositivos(df)
sacar_tuits_horas(df)
