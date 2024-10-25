import pandas as pd
import click
import nltk
import re
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import string
import matplotlib.pyplot as plt

tknzr = nltk.tokenize.TweetTokenizer()

nltk.download('punkt_tab')

def preprocess(text):
    tokens = [t.lower() for t in tknzr.tokenize(text)]
    return tokens

def remove_punctuation(text):
    url_pattern = r'http[s]?://\S+|www\.\S+'
    # Eliminar URLs del texto
    text_without_urls = re.sub(url_pattern, '', text)
    
    # Tokenizar el texto
    tokens = word_tokenize(text_without_urls)
    # Filtrar tokens para eliminar signos de puntuación
    tokens = [token for token in tokens if token not in string.punctuation]
    return tokens

df = pd.read_csv("cyberpunk.csv")
#df["tokens"] = df["text"].apply(preprocess)
df['tokens'] = df['text'].apply(remove_punctuation)

""" all_tokens = [token for tokens_list in df['tokens'] for token in tokens_list]
token_counts = pd.Series(all_tokens).value_counts()

with open('token_counts.txt', 'w') as f:
    f.write(token_counts.to_string())

print(token_counts) """



df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Filtrar la frecuencia de las palabras "good" y "bad"
df['good_count'] = df['tokens'].apply(lambda tokens: tokens.count('good'))
df['bad_count'] = df['tokens'].apply(lambda tokens: tokens.count('bad'))

# Filtrar solo las filas con presencia de "good" o "bad"
df_filtered = df[(df['good_count'] > 0) | (df['bad_count'] > 0)]

# Crear gráfico de polaridad
plt.figure(figsize=(10, 6))

# Graficar la frecuencia de "good" en relación con la polaridad
plt.scatter(df_filtered[df_filtered['good_count'] > 0]['polarity'],
            df_filtered[df_filtered['good_count'] > 0]['good_count'],
            color='green', label='Good')

# Graficar la frecuencia de "bad" en relación con la polaridad
plt.scatter(df_filtered[df_filtered['bad_count'] > 0]['polarity'],
            df_filtered[df_filtered['bad_count'] > 0]['bad_count'],
            color='red', label='Bad')

# Personalización del gráfico
plt.xlabel('Polaridad')
plt.ylabel('Frecuencia')
plt.title('Relación de Polaridad con las Palabras "Good" y "Bad"')
plt.legend()
plt.grid(True)
plt.savefig("grafico_polaridad.png")