import pandas as pd
import click
import nltk
import re
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import string

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

all_tokens = [token for tokens_list in df['tokens'] for token in tokens_list]
token_counts = pd.Series(all_tokens).value_counts()

with open('token_counts.txt', 'w') as f:
    f.write(token_counts.to_string())

print(token_counts)