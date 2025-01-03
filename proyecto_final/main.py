import asyncio
import click
from cargar import cargar
import analisis
from extract import extract_comments_from_json
import descarga
from pathlib import Path
from grafo import generar_grafo_desde_json
import analisis_grafos
import networkx as nx

     
@click.command()
@click.option(
    "-d", "--descargar", is_flag=True, help= "Permite descargar el HTML de un video de YouTube a traves de su URL.\n"
)
@click.option(
    "-a", "--all", is_flag=True, help= "Se ejecutan todas las funciones opcionales.\n"
)
@click.option(
    "-g", "--graficos", is_flag=True, help= "Genera graficos de un JSON en concreto.\n"
)
@click.option(
    "-ga", "--grafo_act", is_flag=True, help= "Genera un grafo que relaciona la actividad de los autores\n"
)
@click.option(
    "-gc", "--grafo_coment", is_flag=True, help= "Genera un grafo que relaciona los comentarios con sus respuestas\n"
)
@click.option(
    "-anlg", "--analisisgrafo", is_flag = True, help = "Analiza de distintas formas el grafo de la actividad de los autores\n"
)
def my_main(graficos, grafo_act, grafo_coment, analisisgrafo, descargar, all):
    '''if (descargar):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(descarga.descargar_html_video())'''
    archivo_json = cargar()
    if graficos or all:
        analisis.generar_graficos(archivo_json)
        fechas_polaridad = analisis.filtrar_y_analizar_palabra_video(archivo_json)
        analisis.graficar_evolucion_palabra_video(fechas_polaridad)

    if grafo_act or all:
        generar_grafo_desde_json(archivo_json, 'actividad_autor')
    
    if grafo_coment or all:
        generar_grafo_desde_json(archivo_json, 'comentarios')

    if analisisgrafo or all:
         # Leer el archivo de red (lista de aristas)
        file = "grafo_actividad_autor.edgelist"
        G = nx.read_edgelist(file)

        # Calcular el nombre base del archivo (sin extensión) para guardar gráficos
        red_social = "grafico_actividad_autor"

        # Cálculo de propiedades del grafo
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
        
    #else:
        # Flujo normal del programa
        # html = cargar()
        # comentarios = extract_comments_from_json(html)
        # print(comentarios)
    #hay que pasar estos comentarios a un analisis.py que lo analiza, es posible que haya que aumentar el extract.py para sacar más datos que analizar

# Ejecución del programa
if __name__ == "__main__":
    my_main()
