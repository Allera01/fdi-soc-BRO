import click
from cargar import cargar
import analisis
import descarga
from grafo import generar_grafo_desde_json
import analisis_grafos
import networkx as nx


@click.command()
@click.option(
    "-d",
    "--descargar",
    is_flag=True,
    help="Permite descargar el HTML de un video de YouTube a traves de su URL.\n",
)
@click.option(
    "-a", "--all", is_flag=True, help="Se ejecutan todas las funciones opcionales.\n"
)
@click.option(
    "-g", "--graficos", is_flag=True, help="Genera graficos de un JSON en concreto.\n"
)
@click.option(
    "-ga",
    "--grafo_act",
    is_flag=True,
    help="Genera un grafo que relaciona la actividad de los autores\n",
)
@click.option(
    "-anlg",
    "--analisisgrafo",
    is_flag=True,
    help="Analiza de distintas formas el grafo de la actividad de los autores\n",
)
def my_main(graficos, grafo_act, analisisgrafo, descargar, all):
    if descargar:
        descarga.descargar()

    archivo_json = cargar()
    if graficos or all:
        analisis.generar_graficos(archivo_json)

    if grafo_act or all:
        generar_grafo_desde_json(archivo_json, "actividad_autor")

    if analisisgrafo or all:
        file = "grafo_actividad_autor.edgelist"
        G = nx.read_edgelist(file)

        red_social = "grafico_actividad_autor"

        num_nodes, num_edges = analisis_grafos.calcular_nodos_y_aristas(G)
        analisis_grafos.calcular_distribucion_grados(G, red_social)
        coef_clust = analisis_grafos.calcular_coeficiente_clustering(G)
        analisis_grafos.visualizar_distribucion_clustering(G, coef_clust, red_social)
        analisis_grafos.calcular_distribucion_conjunta(G, red_social)

        distancia_media = analisis_grafos.calcular_distancia_media(G)
        diametro_red = analisis_grafos.calcular_diametro(G)
        distancias_hubs = analisis_grafos.calcular_distancia_a_hubs(G, red_social)
        show = analisis_grafos.visualizar_red(G, red_social)

        analisis_grafos.generar_informe_markdown(
            red_social,
            file,
            num_nodes,
            num_edges,
            show,
            distancia_media,
            diametro_red,
            distancias_hubs,
        )


# Ejecución del programa
if __name__ == "__main__":
    my_main()
