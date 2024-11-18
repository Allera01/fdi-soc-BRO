import networkx as nx
import matplotlib.pyplot as plt
import os
import click


@click.command()  # Define el comando principal
@click.argument(
    "file", type=click.File("r")
)  # Define argumentos que el usuario debe pasar (en este caso, el archivo de lista de aristas)
def analyze_network(file):
    """Analiza las propiedades básicas de la red usando funciones auxiliares."""
    # Leer el archivo de red (lista de aristas)
    G = nx.read_edgelist(file)

    # Calcular el nombre base del archivo (sin extensión) para guardar gráficos
    red_social = os.path.splitext(os.path.basename(file.name))[0]

    # Cálculo de propiedades del grafo
    calcular_nodos_y_aristas(G)
    calcular_distribucion_grados(G, red_social)
    calcular_coeficiente_clustering(G, red_social)


def calcular_nodos_y_aristas(G):
    """Calcula y muestra el número de nodos y aristas del grafo."""
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    click.echo(f"Número de nodos: {num_nodes}")
    click.echo(f"Número de aristas: {num_edges}")


def calcular_distribucion_grados(G, red_social):
    """Calcula y visualiza la distribución de grados de los nodos."""
    grados = dict(G.degree())
    promedio_grado = sum(grados.values()) / len(grados)

    # Separar entre hubs y no hubs
    hubs = {nodo: grado for nodo, grado in grados.items() if grado > promedio_grado}
    no_hubs = {nodo: grado for nodo, grado in grados.items() if grado <= promedio_grado}

    # Calcular la distribución de grados para hubs y no hubs
    distribucion_hubs = {}
    distribucion_no_hubs = {}
    for nodo, grado in grados.items():
        if grado > promedio_grado:
            distribucion_hubs[grado] = distribucion_hubs.get(grado, 0) + 1
        else:
            distribucion_no_hubs[grado] = distribucion_no_hubs.get(grado, 0) + 1

    # Visualización
    plt.figure(figsize=(8, 6))
    plt.bar(
        distribucion_no_hubs.keys(),
        distribucion_no_hubs.values(),
        color="red",
        label="No Hubs",
    )
    plt.bar(
        distribucion_hubs.keys(), distribucion_hubs.values(), color="blue", label="Hubs"
    )
    plt.xlabel("Grados")
    plt.ylabel("Cantidad")
    plt.title("Distribución de grados de los nodos (Hubs resaltados)")
    plt.legend()
    plt.savefig(f"distribucion_{red_social}_hubs.png")
    plt.close()


def calcular_coeficiente_clustering(G, red_social):
    """Calcula y visualiza la distribución del coeficiente de clustering."""
    coef_clustering = nx.clustering(G)

    # Separar los coeficientes de clustering para hubs y no hubs
    grados = dict(G.degree())
    promedio_grado = sum(grados.values()) / len(grados)
    hubs = {nodo for nodo, grado in grados.items() if grado > promedio_grado}
    no_hubs = {nodo for nodo in G.nodes() if nodo not in hubs}

    clustering_hubs = {
        nodo: coef for nodo, coef in coef_clustering.items() if nodo in hubs
    }
    clustering_no_hubs = {
        nodo: coef for nodo, coef in coef_clustering.items() if nodo in no_hubs
    }

    # Agrupar en intervalos de 0.1
    clustering_bins_hubs = agrupar_clustering(clustering_hubs)
    clustering_bins_no_hubs = agrupar_clustering(clustering_no_hubs)

    # Visualización
    plt.figure(figsize=(8, 6))
    plt.bar(
        clustering_bins_no_hubs.keys(),
        clustering_bins_no_hubs.values(),
        color="red",
        width=0.05,
        label="No Hubs",
    )
    plt.bar(
        clustering_bins_hubs.keys(),
        clustering_bins_hubs.values(),
        color="blue",
        width=0.05,
        label="Hubs",
    )
    plt.xlabel("Coeficiente de Clustering")
    plt.ylabel("Cantidad de Nodos")
    plt.title("Distribución del Coeficiente de Clustering (Hubs resaltados)")
    plt.legend()
    plt.savefig(f"clustering_{red_social}_hubs.png")
    plt.close()


def agrupar_clustering(coeficientes):
    """Agrupa los coeficientes de clustering en intervalos de 0.1."""
    bins = {}
    for coef in coeficientes.values():
        bin = round(coef, 1)
        bins[bin] = bins.get(bin, 0) + 1
    return bins


if __name__ == "__main__":
    analyze_network()
