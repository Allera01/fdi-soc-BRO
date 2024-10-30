import pandas as pd
import click
import nltk
import re
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk import ngrams
from collections import Counter
import string
import matplotlib.pyplot as plt

""" 
tknzr = nltk.tokenize.TweetTokenizer()

nltk.download('punkt_tab')

#Separar las palabras
def preprocess(text):
    tokens = [t.lower() for t in tknzr.tokenize(text)]
    return tokens
 """
#Quitar las URL y los signos de puntuación
def remove_punctuation(text):
    url_pattern = r'http[s]?://\S+|www\.\S+'
    # Eliminar URLs del texto
    text_without_urls = re.sub(url_pattern, '', text)
    # Tokenizar el texto
    tokens = word_tokenize(text_without_urls)
    # Filtrar tokens para eliminar signos de puntuación
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    #tokens = [word for word in words if word.lower() not in stop_words]
    return tokens

def grafico_polaridad_2p(palabra1, palabra2, datos):
    df = datos
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Calcular la longitud del tweet
    df['tweet_length'] = df['text'].apply(len)

    # Filtrar los tweets que contienen las palabras 
    df['contains_palabra1'] = df['tokens'].apply(lambda tokens: palabra1 in tokens)
    df['contains_palabra2'] = df['tokens'].apply(lambda tokens: palabra2 in tokens)

    # Filtrar solo las filas con las palabras
    df_palabra1_palabra2 = df[(df['contains_palabra1']) | (df['contains_palabra2'])]

    # Crear gráfico de polaridad vs longitud del tweet, diferenciando las palabras
    plt.figure(figsize=(10, 6))

    # Graficar tweets con la palabra1
    plt.scatter(df_palabra1_palabra2[df_palabra1_palabra2['contains_palabra1']]['tweet_length'],
                df_palabra1_palabra2[df_palabra1_palabra2['contains_palabra1']]['polarity'],
                color='blue', label=palabra1, alpha=0.5)

    # Graficar tweets con la palabra2
    plt.scatter(df_palabra1_palabra2[df_palabra1_palabra2['contains_palabra2']]['tweet_length'],
                df_palabra1_palabra2[df_palabra1_palabra2['contains_palabra2']]['polarity'],
                color='red', label=palabra2, alpha=0.5)

    # Personalización del gráfico
    plt.xlabel('Longitud del Tweet')
    plt.ylabel('Polaridad')
    plt.title('Relación entre Polaridad y Longitud del Tweet para ' + palabra1 + ' y ' + palabra2)
    plt.legend()
    plt.grid(True)
    plt.savefig("grafico_polaridad_" + palabra1 +"_" + palabra2 +".png")
    
def grafico_polaridad_1p(palabra, datos):
    df = datos
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Calcular la longitud del tweet
    df['tweet_length'] = df['text'].apply(len)

    # Filtrar los tweets que contienen la palabra
    df['contains_palabra'] = df['tokens'].apply(lambda tokens: palabra in tokens)

    # Filtrar solo las filas con la palabra
    df_palabra = df[(df['contains_palabra'])]

    # Crear gráfico de polaridad vs longitud del tweet
    plt.figure(figsize=(10, 6))

    # Graficar tweets con palabra
    plt.scatter(df_palabra[df_palabra['contains_palabra']]['tweet_length'],
                df_palabra[df_palabra['contains_palabra']]['polarity'],
                color='green', label=palabra, alpha=0.5)

    # Personalización del gráfico
    plt.xlabel('Longitud del Tweet')
    plt.ylabel('Polaridad')
    plt.title('Relación entre Polaridad y Longitud del Tweet para '+palabra)
    plt.legend()
    plt.grid(True)
    plt.savefig("grafico_polaridad_" + palabra +".png")
    
df = pd.read_csv("cyberpunk.csv")
#df["tokens"] = df["text"].apply(preprocess)
df['tokens'] = df['text'].apply(remove_punctuation)

#descomentar para tener la lista de palabras junto a su numero de apariciones
"""#Añadir a all_tokens todos los tokens sin repetición
all_tokens = [token for tokens_list in df['tokens'] for token in tokens_list]
#Contar la cantidad de veces que aparece cada token
token_counts = pd.Series(all_tokens).value_counts()

with open('token_counts.txt', 'w') as f:
    f.write(token_counts.to_string())
"""
#print(token_counts) 

bigramas = []
trigramas = []

for tokens in df['tokens']:
    bigramas.extend(ngrams(tokens, 2))  # Generar bigramas
    trigramas.extend(ngrams(tokens, 3))  # Generar trigramas

# Contar frecuencias de bigramas y trigramas
bigramas_frecuentes = Counter(bigramas)
trigramas_frecuentes = Counter(trigramas)

# Mostrar los 10 bigramas y trigramas más comunes
print("Bigramas más comunes:", bigramas_frecuentes.most_common(10))
print("Trigramas más comunes:", trigramas_frecuentes.most_common(10))

#descomentar dependiendo de que imagenes quieras ver
#grafico_polaridad_1p('cyberpunk', df)
#grafico_polaridad_2p('good', 'bad', df)
#grafico_polaridad_2p('steam', 'playstation', df)
#grafico_polaridad_2p('patch','bugs',df)
#grafico_polaridad_2p('graphics','performance',df)
#grafico_polaridad_2p('story', 'gameplay', df)
