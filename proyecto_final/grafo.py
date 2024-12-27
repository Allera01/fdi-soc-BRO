import networkx as nx
import json
import matplotlib.pyplot as plt
from textblob import TextBlob

# def cargar_datos_json(ruta_json):
#     """Carga los datos del archivo JSON especificado."""
#     with open(ruta_json, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     return data

def analizar_polaridad(texto):
    """Devuelve la polaridad de un texto usando TextBlob."""
    blob = TextBlob(texto)
    return blob.sentiment.polarity

def construir_grafo_comentarios(data):
    """Construye un grafo a partir de los comentarios principales y sus respuestas."""
    G = nx.DiGraph()

    comentarios = data[0]['items'][:15]  # Tomar solo los primeros 15 comentarios principales

    for comentario in comentarios:
        if 'snippet' in comentario and 'topLevelComment' in comentario['snippet']:
            top_comment = comentario['snippet']['topLevelComment']['snippet']
            top_comment_id = comentario['id']
            top_comment_text = top_comment['textDisplay']
            top_comment_author = top_comment['authorDisplayName']

            # Añadir nodo para el comentario principal
            G.add_node(
                top_comment_author,
                label=top_comment_text,
                type='author'
            )

            # Añadir nodos para las respuestas si existen
            if 'replies' in comentario:
                for reply in comentario['replies']['comments']:
                    reply_snippet = reply['snippet']
                    reply_author = reply_snippet['authorDisplayName']

                    # Añadir nodo para el autor de la respuesta
                    G.add_node(
                        reply_author,
                        label=reply_snippet['textDisplay'],
                        type='author'
                    )

                    # Añadir arista del autor del comentario principal al autor de la respuesta
                    G.add_edge(top_comment_author, reply_author)

    return G

def graficar_grafo(G, nombre,ruta_guardado=None):
    import numpy as np
    import os
    # Elegir layout
    layouts = {
        'spring': nx.spring_layout,
        'circular': nx.circular_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'random': nx.random_layout
    }
    pos = layouts.get('spring', nx.spring_layout)(G, seed=42)  # Layout reproducible con semilla

    # Configuración de colores según el tipo de nodo
    colors = [
        'blue' if G.nodes[n].get('type', 'unknown') == 'author' else 'red'
        for n in G.nodes
    ]

    # Escalar tamaños de nodos según el grado
    node_sizes = [500 + (np.log1p(G.degree(n)) * 200) for n in G.nodes]

    # Crear etiquetas resumidas para nodos
    labels = {
        n: (G.nodes[n].get('label', n))
        for n in G.nodes
    }

    # Graficar el grafo
    plt.figure(figsize=(30, 30))
    nx.draw(
        G, pos, with_labels=True, labels=labels, node_color=colors,
        node_size=node_sizes, font_size=8, font_color='black',
        edge_color='gray', alpha=0.7
    )
    plt.title(f"Grafo de relaciones (nodos: {len(G.nodes)}, aristas: {len(G.edges)})")

    if not ruta_guardado:
        ruta_guardado = os.path.join(os.getcwd(), nombre + ".png")

    # Guardar grafo en la ruta especificada
    plt.savefig(ruta_guardado, format=ruta_guardado.split('.')[-1])
    
    
    
    # """Genera y muestra un grafo, guardándolo si se proporciona una ruta."""
    # pos = nx.spring_layout(G, seed=42)  # Layout reproducible con semilla

    # # Configuración de colores según el tipo de nodo
    # colors = ['blue' if G.nodes[n].get('type') == 'author' else 'red' for n in G.nodes]

    # # Escalar tamaños de nodos según el grado
    # node_sizes = [500 + (G.degree(n) * 100) for n in G.nodes]

    # # Crear etiquetas resumidas para nodos
    # labels = {
    #     n: G.nodes[n]['label'][:15] + '...' if len(G.nodes[n]['label']) > 15 else G.nodes[n]['label']
    #     for n in G.nodes
    # }

    # plt.figure(figsize=(12, 12))
    # nx.draw(
    #     G, pos, with_labels=True, labels=labels, node_color=colors, cmap=plt.cm.coolwarm,
    #     node_size=node_sizes, font_size=8, font_color='black', edge_color='gray', alpha=0.7
    # )
    # plt.title("Relaciones entre comentarios y respuestas")

    # if ruta_guardado:
    #     plt.savefig(ruta_guardado, format='png')
    # plt.show()

# Función para grafo de actividad del autor
def grafo_actividad_autor(data):    
    """Crea un grafo que conecta autores principales con autores que responden."""
    G = nx.DiGraph()

    for i in range(0,5):
        comentarios = data[i]['items']
        for comentario in comentarios:
            if 'snippet' in comentario and 'topLevelComment' in comentario['snippet']:
                top_comment = comentario['snippet']['topLevelComment']['snippet']
                top_comment_author = top_comment['authorDisplayName']
                
                if not G.has_node(top_comment_author):
                    G.add_node(top_comment_author, type='author')

                if 'replies' in comentario:
                    for reply in comentario['replies']['comments']:
                        reply_author = reply['snippet']['authorDisplayName']

                        if not G.has_node(reply_author):
                            G.add_node(reply_author, type='author')

                        if not G.has_edge(top_comment_author, reply_author):
                            G.add_edge(top_comment_author, reply_author)
        
    graficar_grafo(G, "actividad_del_autor")

# Función para grafo de sentimiento agregado por autor
def grafo_sentimiento_autor(data):
    """Crea un grafo donde las aristas tienen pesos basados en el sentimiento promedio."""
    G = nx.DiGraph()

    for i in range(0,5):
        comentarios = data[i]['items']

        for comentario in comentarios:
            if 'snippet' in comentario and 'topLevelComment' in comentario['snippet']:
                top_comment = comentario['snippet']['topLevelComment']['snippet']
                top_comment_author = top_comment['authorDisplayName']

                G.add_node(top_comment_author, type='author')

                if 'replies' in comentario:
                    for reply in comentario['replies']['comments']:
                        reply_snippet = reply['snippet']
                        reply_author = reply_snippet['authorDisplayName']
                        reply_polarity = analizar_polaridad(reply_snippet['textDisplay'])

                        G.add_node(reply_author, type='author')

                        if G.has_edge(top_comment_author, reply_author):
                            G[top_comment_author][reply_author]['weight'] += reply_polarity
                            G[top_comment_author][reply_author]['count'] += 1
                        else:
                            G.add_edge(
                                top_comment_author, reply_author,
                                weight=reply_polarity, count=1
                            )

    # Ajustar los pesos finales como el promedio de polaridades
    for u, v, data in G.edges(data=True):
        data['weight'] = data['weight'] / data['count']

    graficar_grafo(G, "sentimiento_autor")

# Función principal para generar el grafo desde JSON
def generar_grafo_desde_json(nombre_json, tipo_grafo):
    """Carga datos de un JSON, genera el tipo de grafo seleccionado y lo grafica."""
    # ruta_json = f"{nombre_json}"
    # datos = cargar_datos_json(ruta_json)
    datos = json.loads(nombre_json)

    if tipo_grafo == 'actividad_autor':
        grafo_actividad_autor(datos)
    elif tipo_grafo == 'sentimiento_autor':
        grafo_sentimiento_autor(datos)
    else:
        raise ValueError("Tipo de grafo no reconocido. Usa 'actividad_autor' o 'sentimiento_autor'.")
