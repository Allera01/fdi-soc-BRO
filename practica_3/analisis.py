import networkx as nx
import matplotlib.pyplot as plt
import click
from string import Template
import os


def calcular_nodos_y_aristas(G):
    """Calcula y muestra el número de nodos y aristas del grafo."""
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    click.echo(f"Número de nodos: {num_nodes}")
    click.echo(f"Número de aristas: {num_edges}")
    return num_nodes, num_edges

def calcular_distribucion_grados(G, red_social):
    """Calcula y visualiza la distribución de grados de los nodos."""
    if not os.path.isfile(f"distribucion_{red_social}_hubs.png"):
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

'''def calcular_coeficiente_clustering(G, red_social):
    """Calcula y visualiza la distribución del coeficiente de clustering."""
    if not os.path.isfile(f"clustering_{red_social}_hubs.png"):
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
        plt.close()'''



def calcular_coeficiente_clustering(G, red_social):
    """Calcula manualmente y visualiza la distribución del coeficiente de clustering."""
    if not os.path.isfile(f"clustering_{red_social}_hubs.png"):
        # Calcular coeficientes de clustering manualmente
        coef_clustering = {}
        for nodo in G:
            vecinos = list(G[nodo])  # Obtener vecinos del nodo
            grado = len(vecinos)
            
            # Si el grado es menor que 2, el coeficiente de clustering es 0
            if grado < 2:
                coef_clustering[nodo] = 0.0
                continue
            
            # Contar triángulos
            triángulos = 0
            for i, vecino1 in enumerate(vecinos):
                for vecino2 in vecinos[i+1:]:
                    if vecino2 in G[vecino1]:  # Si hay arista entre vecino1 y vecino2
                        triángulos += 1
            
            # Calcular el coeficiente de clustering
            coef_clustering[nodo] = (2 * triángulos) / (grado * (grado - 1))
        
        # Separar nodos en hubs y no hubs
        grados = {nodo: len(G[nodo]) for nodo in G}
        promedio_grado = sum(grados.values()) / len(grados)
        hubs = {nodo for nodo, grado in grados.items() if grado > promedio_grado}
        no_hubs = {nodo for nodo in G if nodo not in hubs}
        
        clustering_hubs = {
            nodo: coef for nodo, coef in coef_clustering.items() if nodo in hubs
        }
        clustering_no_hubs = {
            nodo: coef for nodo, coef in coef_clustering.items() if nodo in no_hubs
        }
        
        # Agrupar coeficientes de clustering en intervalos
        def agrupar_clustering(clustering, bin_size=0.1):
            bins = {}
            for coef in clustering.values():
                bin_intervalo = round(coef // bin_size * bin_size, 2)  # Redondear al bin más cercano
                bins[bin_intervalo] = bins.get(bin_intervalo, 0) + 1
            return bins
        
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

def calcular_distribucion_conjunta(G, red_social):
    """Genera la distribución conjunta de grados y coeficientes de clustering."""
    if not os.path.isfile(f"distribucion_conjunta_{red_social}.png"):
        grados = dict(G.degree())
        coef_clustering = nx.clustering(G)

        # Separar en hubs y no hubs
        promedio_grado = sum(grados.values()) / len(grados)
        hubs = {nodo for nodo, grado in grados.items() if grado > promedio_grado}
        no_hubs = {nodo for nodo in G.nodes() if nodo not in hubs}

        # Preparar los datos para los subgráficos
        grados_hubs = [grados[nodo] for nodo in hubs]
        grados_no_hubs = [grados[nodo] for nodo in no_hubs]
        clustering_hubs = {
            nodo: coef for nodo, coef in coef_clustering.items() if nodo in hubs
        }
        clustering_no_hubs = {
            nodo: coef for nodo, coef in coef_clustering.items() if nodo in no_hubs
        }

        # Agrupar los coeficientes de clustering usando la función 'agrupar_clustering'
        clustering_bins_hubs = agrupar_clustering(clustering_hubs)
        clustering_bins_no_hubs = agrupar_clustering(clustering_no_hubs)

        # Crear subgráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Gráfico de grados
        ax1.hist(grados_hubs, bins=range(min(grados_hubs), max(grados_hubs) + 1), color="blue", alpha=0.7, label="Hubs")
        ax1.hist(grados_no_hubs, bins=range(min(grados_no_hubs), max(grados_no_hubs) + 1), color="red", alpha=0.7, label="No Hubs")
        ax1.set_title("Distribución de Grados")
        ax1.set_xlabel("Grado")
        ax1.set_ylabel("Cantidad de Nodos")
        ax1.legend()

        # Gráfico de coeficientes de clustering utilizando los bins calculados
        ax2.bar(
            clustering_bins_no_hubs.keys(),
            clustering_bins_no_hubs.values(),
            color="red", width=0.05, label="No Hubs"
        )
        ax2.bar(
            clustering_bins_hubs.keys(),
            clustering_bins_hubs.values(),
            color="blue", width=0.05, label="Hubs"
        )
        ax2.set_title("Distribución del Coeficiente de Clustering")
        ax2.set_xlabel("Coeficiente de Clustering")
        ax2.set_ylabel("Cantidad de Nodos")
        ax2.legend()

        # Guardar la figura como un archivo PNG
        plt.tight_layout()
        plt.savefig(f"distribucion_conjunta_{red_social}.png")
        plt.close()

def generar_informe_markdown(red_social, archivo, numero_nodes, numero_edges):
    """Genera un informe en Markdown con los resultados y gráficos obtenidos del análisis de la red."""
    if not os.path.isfile(f"{red_social}_informe.md"):
        # Cargar los resultados de los cálculos realizados (esto debe estar basado en las salidas generadas por las funciones)
        # Por ejemplo, los valores de número de nodos y aristas, distribución de grados, coeficiente de clustering, etc.
        
        # Suponiendo que estos valores se obtienen durante el proceso de análisis
        num_nodes = numero_nodes  # Número de nodos
        num_edges = numero_edges  # Número de aristas
        distribucion_grados_path = f"distribucion_{red_social}_hubs.png"
        coef_clustering_path = f"clustering_{red_social}_hubs.png"
        distribucion_conjunta_path = f"distribucion_conjunta_{red_social}.png"
        
        # Plantilla Markdown para el informe
        markdown_template = Template("""
    # Informe de Análisis de la Red Social

    ## Resumen
    Este informe presenta el análisis de una red social representada en el archivo ${archivo}. A continuación se detallan las propiedades básicas de la red y visualizaciones de los resultados obtenidos.

    ### Propiedades Básicas de la Red
    - **Número de nodos**: ${num_nodes}
    - **Número de aristas**: ${num_edges}

    ## Gráficos

    ### 1. Distribución de Grados de los Nodos
    Este gráfico muestra la distribución de los grados de los nodos, con una distinción entre los nodos "hubs" (con mayor grado) y los "no hubs":

    ![Distribución de Grados](./${distribucion_grados_path})

    ### 2. Distribución del Coeficiente de Clustering
    El siguiente gráfico presenta la distribución del coeficiente de clustering, diferenciando entre los hubs y los nodos de menor grado:

    ![Coeficiente de Clustering](./${coef_clustering_path})

    ### 3. Distribución Conjunta de Grados y Coeficiente de Clustering
    Este gráfico muestra la distribución conjunta de los grados y los coeficientes de clustering, proporcionando una visión más detallada sobre la relación entre estas dos métricas en la red social:

    ![Distribución Conjunta](./${distribucion_conjunta_path})

    ## Conclusiones
    A partir de los análisis anteriores, podemos extraer varias conclusiones:

    - La red tiene ${num_nodes} nodos y ${num_edges} aristas.
    - La distribución de grados muestra una clara diferencia entre los nodos hubs y los nodos no hubs, lo que indica la existencia de una estructura de red jerárquica.
    - La distribución del coeficiente de clustering indica que los hubs tienden a estar más conectados entre sí, formando comunidades más cohesionadas.
    """)
        
        # Rellenar la plantilla con los datos
        informe_markdown = markdown_template.substitute(
            archivo=archivo.name,
            red_social=red_social,
            num_nodes=num_nodes,
            num_edges=num_edges,
            distribucion_grados_path=distribucion_grados_path,
            coef_clustering_path=coef_clustering_path,
            distribucion_conjunta_path=distribucion_conjunta_path
        )
        
        # Guardar el informe en un archivo Markdown
        output_filename = f"{red_social}_informe.md"
        with open(output_filename, "w") as f:
            f.write(informe_markdown)
        
        print(f"Informe generado exitosamente: {output_filename}")

def visualizar_red(G, red_social):
    """Genera una visualización de la red destacando los 300 nodos con más aristas (grados)."""
    if not os.path.isfile(f"visualizacion_{red_social}_hubs.png"):
        # Calcular los grados de los nodos
        grados = dict(G.degree())
        
        # Ordenar nodos por grado en orden descendente y tomar los 300 con mayor grado
        nodos_top = sorted(grados, key=grados.get, reverse=True)[:1000]
        
        # Crear un subgrafo con los 300 nodos seleccionados
        subgrafo = G.subgraph(nodos_top)
        
        # Calcular grados en el subgrafo
        grados_subgrafo = dict(subgrafo.degree())
        promedio_grado = sum(grados_subgrafo.values()) / len(grados_subgrafo)
        
        # Identificar hubs y no hubs en el subgrafo
        hubs = {nodo: grado for nodo, grado in grados_subgrafo.items() if grado > promedio_grado}
        no_hubs = {nodo: grado for nodo, grado in grados_subgrafo.items() if grado <= promedio_grado}

        # Asignar tamaños y colores a los nodos
        tamanos = [
            grados_subgrafo[nodo] if nodo in hubs else grados_subgrafo[nodo]
            for nodo in subgrafo.nodes()
        ]
        colores = ["blue" if nodo in hubs else "red" for nodo in subgrafo.nodes()]

        # Dibujar la red
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(subgrafo, seed=42)  # Layout de la red
        nx.draw(
            subgrafo,
            pos,
            with_labels=False,
            node_size=tamanos,
            node_color=colores,
            edge_color="gray",
            alpha=0.7,
        )
        plt.title("Visualización de la Red con Hubs Destacados")
        plt.savefig(f"visualizacion_{red_social}_hubs.png")
        plt.close()

        click.echo(f"Visualización de la red guardada como: visualizacion_{red_social}_hubs.png")

def calcular_distancia_media(G, red_social):

    # Calcular los grados de los nodos
    grados = dict(G.degree())
        
    # Ordenar nodos por grado en orden descendente y tomar los 300 con mayor grado
    nodos_top = sorted(grados, key=grados.get, reverse=True)[:1000]
        
    # Crear un subgrafo con los 300 nodos seleccionados
    sub = G.subgraph(nodos_top)

    """Calcula la distancia media entre pares de nodos."""
    # Comprobamos si el grafo es conexo
    if nx.is_connected(sub):
        # Si es conexo, calculamos la distancia media de los nodos
        distancia_media = nx.average_shortest_path_length(sub)
        click.echo(f"La distancia media entre pares de nodos es: {distancia_media :.2f} aristas y el grafo es conexo")
    else:
        # Si no es conexo, calculamos la distancia media para cada componente conexo
        componentes_conexos = list(nx.connected_components(sub))
        distancias_componentes = []
        
        for componente in componentes_conexos:
            subgrafo = sub.subgraph(componente)
            try:
                distancias_componentes.append(nx.average_shortest_path_length(subgrafo))
            except nx.NetworkXError:
                # Si el subgrafo no tiene al menos dos nodos, no se puede calcular la distancia media
                continue
        
        if distancias_componentes:
            distancia_media_promedio = sum(distancias_componentes) / len(distancias_componentes)
            click.echo(f"La distancia media entre pares de nodos en los componentes conexos es: {distancia_media_promedio:.2f} aristas y el grafo es no conexo")
        else:
            click.echo("No se pudo calcular la distancia media debido a componentes desconectados demasiado pequeños.")

def calcular_diametro(G):
    """Calcula y muestra el diámetro de la red."""
    diametro = nx.diameter(G)
    click.echo(f"El diámetro de la red es: {diametro}")

def calcular_distancia_a_hubs(G, red_social):
    """Calcula la distribución de distancias desde los nodos a los hubs."""
    if not os.path.isfile(f"distribucion_distancias_{red_social}_hubs.png"):
        # Identificar los hubs
        grados = dict(G.degree())
        promedio_grado = sum(grados.values()) / len(grados)
        hubs = {nodo for nodo, grado in grados.items() if grado > promedio_grado}
        
        # Calcular las distancias más cortas desde cada nodo a los hubs
        distancias_a_hubs = {}
        for nodo in G.nodes():
            # Usamos el algoritmo de Dijkstra para encontrar la distancia más corta al nodo hub más cercano
            dist_min = min(nx.single_source_dijkstra_path_length(G, nodo).get(hub, float('inf')) for hub in hubs)
            distancias_a_hubs[nodo] = dist_min
        
        # Generar la distribución de distancias
        distribucion_distancias = {}
        for distancia in distancias_a_hubs.values():
            distribucion_distancias[distancia] = distribucion_distancias.get(distancia, 0) + 1
        
        # Visualización de la distribución de distancias
        plt.figure(figsize=(8, 6))
        plt.bar(distribucion_distancias.keys(), distribucion_distancias.values(), color="green")
        plt.xlabel("Distancia al hub más cercano")
        plt.ylabel("Cantidad de Nodos")
        plt.title(f"Distribución de Distancias a los Hubs en la Red {red_social}")
        plt.savefig(f"distribucion_distancias_{red_social}_hubs.png")
        plt.close()

        click.echo(f"Distribución de distancias calculada y guardada como 'distribucion_distancias_{red_social}_hubs.png'")