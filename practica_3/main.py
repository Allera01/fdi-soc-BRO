import networkx as nx
import matplotlib.pyplot as plt
import os
import click
from string import Template
import analisis


@click.command(help="Este programa analiza propiedades de una red de grafos usando un archivo de lista de aristas.\n")  # Define el comando principal
@click.argument(
    "file", type=click.File("r")
)  
@click.option(
    "-m", "--mostrar", is_flag = True, help = "Muestra una visualización de la red destacando los hubs.\n"
) 
@click.option(
    "-dist", "--distancia", is_flag = True, help = "Muestra la distancia media entre dos nodos del grafo.\n"
)
@click.option(
    "-diam", "--diametro", is_flag = True, help = "Calcular el diámetro de la red, es decir, la longitud del máximo camino más corto entre pares de nodos cualesquiera.\n"
)
@click.option(
    "-dh", "--distanciahubs", is_flag = True, help = "Calcular la distribución de distancias desde los nodos a cada uno de los hubs, lo que da una idea de la “centralidad” de estos.\n"
)
@click.option(
    "-a", "--all", is_flag = True, help = "Se ejecutan todas las funciones opcionales.\n"
)
# Define argumentos que el usuario debe pasar (en este caso, el archivo de lista de aristas)
def my_main(file, mostrar, distancia, diametro, distanciahubs, all):
    """Analiza las propiedades básicas de la red usando funciones auxiliares."""
    # Leer el archivo de red (lista de aristas)
    G = nx.read_edgelist(file)

    # Calcular el nombre base del archivo (sin extensión) para guardar gráficos
    red_social = os.path.splitext(os.path.basename(file.name))[0]

    # Cálculo de propiedades del grafo
    num_nodes, num_edges = analisis.calcular_nodos_y_aristas(G)
    analisis.calcular_distribucion_grados(G, red_social)
    coef_clust = analisis.calcular_coeficiente_clustering(G)
    analisis.visualizar_distribucion_clustering(G, coef_clust, red_social)
    analisis.calcular_distribucion_conjunta(G, red_social)
    analisis.generar_informe_markdown(red_social, file, num_nodes, num_edges)
    
    if mostrar or all:
        analisis.visualizar_red(G, red_social)

    if distancia or all:
        analisis.calcular_distancia_media(G)
    
    if diametro or all:
        analisis.calcular_diametro(G)

    if distanciahubs or all:
        analisis.calcular_distancia_a_hubs(G, red_social)

if __name__ == "__main__":
    my_main()
