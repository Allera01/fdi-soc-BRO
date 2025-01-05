import networkx as nx
import json
import matplotlib.pyplot as plt
from textblob import TextBlob
import numpy as np
import os

def analizar_polaridad(texto):
    """Devuelve la polaridad de un texto usando TextBlob."""
    blob = TextBlob(texto)
    return blob.sentiment.polarity


def graficar_grafo(G, nombre,ruta_guardado=None):
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
    

def guardar_digrafo_edgelist_en_actual(G, nombre_archivo):
    """
    Guarda un grafo dirigido (nx.DiGraph) en formato .edgelist en el directorio actual, si no existe ya el archivo.
    
    Args:
        G (nx.DiGraph): El grafo dirigido a guardar.
        nombre_archivo (str): El nombre del archivo .edgelist donde se guardará.
    """
    # Verificar si el archivo ya existe en el directorio actual
    if os.path.exists(nombre_archivo):
        print(f"El archivo {nombre_archivo} ya existe en el directorio actual. No se ha creado un nuevo archivo.")
        return
    
    # Guardar el grafo dirigido en el archivo
    with open(nombre_archivo, 'w') as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")
    
    print(f"Grafo dirigido guardado exitosamente en {nombre_archivo}")

def grafo_actividad_autor(data):
    """Crea un grafo que conecta autores principales con autores que responden."""
    G = nx.DiGraph()

    for i in range(len(data)):
        comentarios = data[i]['items']
        for comentario in comentarios:
            if 'snippet' in comentario and 'topLevelComment' in comentario['snippet']:
                top_comment = comentario['snippet']['topLevelComment']['snippet']
                top_comment_author = top_comment['authorDisplayName']
                
                # Añadir nodo para el autor principal
                if not G.has_node(top_comment_author):
                    G.add_node(top_comment_author, type='author')

                # Añadir nodos y aristas para las respuestas
                if 'replies' in comentario:
                    for reply in comentario['replies']['comments']:
                        reply_author = reply['snippet']['authorDisplayName']

                        if not G.has_node(reply_author):
                            G.add_node(reply_author, type='author')

                        if not G.has_edge(top_comment_author, reply_author):
                            G.add_edge(top_comment_author, reply_author)

    # Calcular los grados de los nodos
    grados = dict(G.degree())

    # Ordenar nodos por grado en orden descendente y tomar los 300 con mayor grado
    nodos_top = sorted(grados, key=grados.get, reverse=True)[:1000]

    # Crear un subgrafo con los 300 nodos seleccionados
    subgrafo = G.subgraph(nodos_top)
    
    # Guardar el grafo en un archivo .edgelist
    guardar_digrafo_edgelist_en_actual(G, "grafo_actividad_autor.edgelist")

    # Graficar el grafo
    graficar_grafo(subgrafo, "actividad_del_autor")

# Función principal para generar el grafo desde JSON
def generar_grafo_desde_json(nombre_json, tipo_grafo):
    """Carga datos de un JSON, genera el tipo de grafo seleccionado y lo grafica."""
    datos = json.loads(nombre_json)

    if tipo_grafo == 'actividad_autor':
        G = grafo_actividad_autor(datos)
        if(os.path.exists("actividad_del_autor")):
            print("El archivo ya existe\n")
            guardar_digrafo_edgelist_en_actual(G, "actividad_autor.edgelist")
    else:
        raise ValueError("Tipo de grafo no reconocido.")
