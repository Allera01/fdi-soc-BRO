import matplotlib 
matplotlib.use('Agg')

import ipysigma
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt 
from ipysigma import Sigma

df = pd.read_csv('usuarios.csv')

df['karma'] = pd.to_numeric(df['karma'], errors='coerce')
G = nx.Graph()

for index, row in df.iterrows():
        G.add_node(row['nombre'], karma=row['karma'],posts=row['posts'], comentarios=row['comentarios'])

for i in range(len(df)):
    for j in range(i+1, len(df)):
        if df.iloc[i]['karma'] > 100 and df.iloc[j]['karma'] > 100:
                G.add_edge(df.iloc[i]['nombre'], df.iloc[j]['nombre'])

sigma_graph = ipysigma.Sigma(G)
sigma_graph
