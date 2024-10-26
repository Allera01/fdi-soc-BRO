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

#Separar las palabras
def preprocess(text):
    tokens = [t.lower() for t in tknzr.tokenize(text)]
    return tokens

#Quitar las URL y los signos de puntuación
def remove_punctuation(text):
    url_pattern = r'http[s]?://\S+|www\.\S+'
    # Eliminar URLs del texto
    text_without_urls = re.sub(url_pattern, '', text)
    
    # Tokenizar el texto
    tokens = word_tokenize(text_without_urls)
    # Filtrar tokens para eliminar signos de puntuación
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    return tokens

df = pd.read_csv("cyberpunk.csv")
#df["tokens"] = df["text"].apply(preprocess)
df['tokens'] = df['text'].apply(remove_punctuation)

#Añadir a all_tokens todos los tokens sin repetición
all_tokens = [token for tokens_list in df['tokens'] for token in tokens_list]
#Contar la cantidad de veces que aparece cada token
token_counts = pd.Series(all_tokens).value_counts()

with open('token_counts.txt', 'w') as f:
    f.write(token_counts.to_string())
"""
print(token_counts) """



df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Calcular la longitud del tweet
df['tweet_length'] = df['text'].apply(len)

# Filtrar los tweets que contienen las palabras "good" o "bad"
df['contains_good'] = df['tokens'].apply(lambda tokens: 'cyberpunk' in tokens)
#df['contains_bad'] = df['tokens'].apply(lambda tokens: 'character' in tokens)

# Filtrar solo las filas con "good" o "bad"
#df_good_bad = df[(df['contains_good']) | (df['contains_bad'])]
df_good_bad = df[(df['contains_good'])]

# Crear gráfico de polaridad vs longitud del tweet, diferenciando "good" y "bad"
plt.figure(figsize=(10, 6))

# Graficar tweets con "good"
plt.scatter(df_good_bad[df_good_bad['contains_good']]['tweet_length'],
            df_good_bad[df_good_bad['contains_good']]['polarity'],
            color='green', label='cyberpunk', alpha=0.5)

# Graficar tweets con "bad"
#plt.scatter(df_good_bad[df_good_bad['contains_bad']]['tweet_length'],
            #df_good_bad[df_good_bad['contains_bad']]['polarity'],
            #color='red', label='character', alpha=0.5)

# Personalización del gráfico
plt.xlabel('Longitud del Tweet')
plt.ylabel('Polaridad')
plt.title('Relación entre Polaridad y Longitud del Tweet para "Good" y "Bad"')
plt.legend()
plt.grid(True)
plt.savefig("grafico_polaridad.png")