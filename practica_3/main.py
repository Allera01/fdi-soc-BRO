import networkx as nx
import matplotlib.pyplot as plt
import os
import click

@click.command()
@click.argument('file', type=click.File('r'))

def analyze_network(file):
    """Calcula propiedades básicas de la red."""
    # Leer el archivo de red (usando el archivo ya abierto)
    G = nx.read_edgelist(file)

    """Calcular y mostrar el número de nodos y aristas"""
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    click.echo(f"Número de nodos: {num_nodes}")
    click.echo(f"Número de enlaces: {num_edges}")

    """Calcular y mostrar la distribución de grados de los nodos"""
    grados = dict(G.degree())

    # Promedio de grados
    promedio_grado = sum(grados.values()) / len(grados) 

    # Separar entre hubs y no hubs
    hubs = {nodo: grado for nodo, grado in grados.items() if grado > promedio_grado}
    no_hubs = {nodo: grado for nodo, grado in grados.items() if grado <= promedio_grado}

    # Distribución de grados para hubs y no hubs
    distribucion_hubs = {}
    distribucion_no_hubs = {}
    for nodo, grado in grados.items():
        if grado > promedio_grado:
            distribucion_hubs[grado] = distribucion_hubs.get(grado, 0) + 1
        else:
            distribucion_no_hubs[grado] = distribucion_no_hubs.get(grado, 0) + 1
        
    # Visualizar la distribución de grados con identificación de hubs
    plt.figure(figsize=(8, 6))
    plt.bar(distribucion_no_hubs.keys(), distribucion_no_hubs.values(), color='red', label='No Hubs')
    plt.bar(distribucion_hubs.keys(), distribucion_hubs.values(), color='blue', label='Hubs')
    plt.xlabel("Grados")
    plt.ylabel("Cantidad")
    plt.title("Distribución de grados de los nodos (Hubs resaltados)")
    plt.legend()
    #Extraer el nombre base del archivo (sin extensión)
    red_social = os.path.splitext(os.path.basename(file))[0]
    plt.savefig("distribucion_{red_social}_hubs.png")

    """Calcular y mostrar la distribución de coeficientes de clústering"""
    # Cálculo del coeficiente de clustering
    coef_clustering = nx.clustering(G)

    # Identificar los coeficientes de clustering para hubs y no hubs
    clustering_hubs = {nodo: coef for nodo, coef in coef_clustering.items() if nodo in hubs}
    clustering_no_hubs = {nodo: coef for nodo, coef in coef_clustering.items() if nodo in no_hubs}

    clustering_bins_hubs = agrupar_clustering(clustering_hubs)
    clustering_bins_no_hubs = agrupar_clustering(clustering_no_hubs)

    # Visualizar la distribución de coeficientes de clustering con identificación de hubs
    plt.figure(figsize=(8, 6))
    plt.bar(clustering_bins_no_hubs.keys(), clustering_bins_no_hubs.values(), color='red', width=0.05, label='No Hubs')
    plt.bar(clustering_bins_hubs.keys(), clustering_bins_hubs.values(), color='blue', width=0.05, label='Hubs')
    plt.xlabel("Coeficiente de Clustering")
    plt.ylabel("Cantidad de Nodos")
    plt.title("Distribución del Coeficiente de Clustering (Hubs resaltados)")
    plt.legend()
    plt.savefig("clustering_{red_social}_hubs.png")

"""Agrupar los coeficientes de clustering en intervalos"""
def agrupar_clustering(coeficientes):
    bins = {}
    for coef in coeficientes.values():
        bin = round(coef, 1)  # Agrupar en intervalos de 0.1
        bins[bin] = bins.get(bin, 0) + 1
    return bins

if __name__ == '__main__':
    analyze_network()