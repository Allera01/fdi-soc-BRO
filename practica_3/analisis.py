import networkx as nx
import matplotlib.pyplot as plt
import click
from string import Template
import os
import random
from collections import deque


def calcular_nodos_y_aristas(G):
    """Calcula y muestra el número de nodos y aristas del grafo."""
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    click.echo(f"Número de nodos: {num_nodes}")
    click.echo(f"Número de aristas: {num_edges}")
    return num_nodes, num_edges


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


def calcular_coeficiente_clustering(G):
    """Calcula manualmente el coeficiente de clustering para cada nodo en el grafo."""

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
            for vecino2 in vecinos[i + 1 :]:
                if vecino2 in G[vecino1]:  # Si hay arista entre vecino1 y vecino2
                    triángulos += 1

        # Calcular el coeficiente de clustering
        coef_clustering[nodo] = (2 * triángulos) / (grado * (grado - 1))

    return coef_clustering


def agrupar_clustering(coeficientes):
    """Agrupa los coeficientes de clustering en intervalos de 0.1."""
    bins = {}
    for coef in coeficientes.values():
        bin = round(coef, 1)
        bins[bin] = bins.get(bin, 0) + 1
    return bins


def visualizar_distribucion_clustering(G, coef_clustering, red_social):
    """Visualiza y guarda la distribución del coeficiente de clustering."""

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
            bin_intervalo = round(
                coef // bin_size * bin_size, 2
            )  # Redondear al bin más cercano
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


def calcular_distribucion_conjunta(G, red_social):
    """Genera la distribución conjunta de grados y coeficientes de clustering."""

    grados = dict(G.degree())
    coef_clustering = calcular_coeficiente_clustering(G)

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
    ax1.hist(
        grados_hubs,
        bins=range(min(grados_hubs), max(grados_hubs) + 1),
        color="blue",
        alpha=0.7,
        label="Hubs",
    )
    ax1.hist(
        grados_no_hubs,
        bins=range(min(grados_no_hubs), max(grados_no_hubs) + 1),
        color="red",
        alpha=0.7,
        label="No Hubs",
    )
    ax1.set_title("Distribución de Grados")
    ax1.set_xlabel("Grado")
    ax1.set_ylabel("Cantidad de Nodos")
    ax1.legend()

    # Gráfico de coeficientes de clustering utilizando los bins calculados
    ax2.bar(
        clustering_bins_no_hubs.keys(),
        clustering_bins_no_hubs.values(),
        color="red",
        width=0.05,
        label="No Hubs",
    )
    ax2.bar(
        clustering_bins_hubs.keys(),
        clustering_bins_hubs.values(),
        color="blue",
        width=0.05,
        label="Hubs",
    )
    ax2.set_title("Distribución del Coeficiente de Clustering")
    ax2.set_xlabel("Coeficiente de Clustering")
    ax2.set_ylabel("Cantidad de Nodos")
    ax2.legend()

    # Guardar la figura como un archivo PNG
    plt.tight_layout()
    plt.savefig(f"distribucion_conjunta_{red_social}.png")
    plt.close()


def generar_informe_markdown(
    red_social,
    file,
    numero_nodes,
    numero_edges,
    m,
    distancia_media,
    diametro_red,
    distancias_hubs,
):
    """Genera un informe en Markdown con los resultados y gráficos obtenidos del análisis de la red."""

    # Cargar los resultados de los cálculos realizados (esto debe estar basado en las salidas generadas por las funciones)
    # Por ejemplo, los valores de número de nodos y aristas, distribución de grados, coeficiente de clustering, etc.

    num_nodes = numero_nodes  # Número de nodos
    num_edges = numero_edges  # Número de aristas
    distribucion_grados_path = f"distribucion_{red_social}_hubs.png"
    coef_clustering_path = f"clustering_{red_social}_hubs.png"
    distribucion_conjunta_path = f"distribucion_conjunta_{red_social}.png"

    # Plantilla Markdown para el informe
    markdown_template = Template(
        """
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

${seccion_mostrar}
${seccion_distancia}
${seccion_diametro}
${seccion_distancia_hubs}

## Conclusiones
A partir de los análisis anteriores, podemos extraer varias conclusiones:

- La red tiene ${num_nodes} nodos y ${num_edges} aristas.
${conclusiones_extra}
    """
    )

    # Secciones condicionales según las opciones de la terminal
    seccion_mostrar = ""
    seccion_distancia = ""
    seccion_diametro = ""
    seccion_distancia_hubs = ""
    conclusiones_extra = ""

    # Si la opción --mostrar está activada
    if m == True:
        seccion_mostrar = f"""
### Visualización de la Red Social
Esta visualización destaca los hubs (nodos con mayor grado) de la red.

![Red Social con Hubs](./visualizacion_{red_social}_hubs.png)
"""

    # Si la opción --distancia está activada
    if distancia_media != None:
        seccion_distancia = f"""
### Distancia Media entre Nodos
La distancia media entre los nodos seleccionados es de **{distancia_media:.2f}**.

"""

    # Si la opción --diametro está activada
    if diametro_red != None:
        seccion_diametro = f"""
### Diámetro de la Red
El diámetro de la red es **{diametro_red:.2f}**, lo que indica la distancia máxima entre dos nodos cualesquiera en la red.
"""

    # Si la opción --distanciahubs está activada
    if distancias_hubs:
        # Mostrar la distribución de distancias
        distribucion_hubs_str = "\n".join(
            [
                f"Distancia: {distancia}, Cantidad de Nodos: {cantidad}"
                for distancia, cantidad in distancias_hubs.items()
            ]
        )
        seccion_distancia_hubs = f"""
### Distribución de Distancias a los Hubs
Este gráfico muestra las distancias desde cada nodo a los hubs, proporcionando información sobre la centralidad de los nodos en la red.

Distribución de distancias a los hubs:
{distribucion_hubs_str}

"""

    # Conclusiones adicionales basadas en las opciones seleccionadas
    if m == True:
        conclusiones_extra += "- Se visualizan los hubs de la red, lo que ayuda a entender su estructura centralizada.\n"
    if distancia_media != None:
        conclusiones_extra += (
            f"- La distancia media entre nodos es de **{distancia_media:.2f}**.\n"
        )
    if diametro_red != None:
        conclusiones_extra += f"- El diámetro de la red es **{diametro_red:.2f}**, indicando una red de gran alcance.\n"
    if distancias_hubs:
        conclusiones_extra += "- La distribución de distancias a los hubs muestra cómo los nodos más cercanos a los hubs son más centrales.\n"

    # Rellenar la plantilla con los datos
    informe_markdown = markdown_template.substitute(
        archivo=file.name,
        red_social=red_social,
        num_nodes=num_nodes,
        num_edges=num_edges,
        seccion_mostrar=seccion_mostrar,
        seccion_distancia=seccion_distancia,
        seccion_diametro=seccion_diametro,
        seccion_distancia_hubs=seccion_distancia_hubs,
        distribucion_grados_path=distribucion_grados_path,
        coef_clustering_path=coef_clustering_path,
        distribucion_conjunta_path=distribucion_conjunta_path,
        conclusiones_extra=conclusiones_extra,
    )

    # Guardar el informe en un archivo Markdown
    output_filename = f"{red_social}_informe.md"
    with open(output_filename, "w") as f:
        f.write(informe_markdown)

    print(f"Informe generado exitosamente: {output_filename}")


def visualizar_red(G, red_social):
    """Genera una visualización de la red destacando los 300 nodos con más aristas (grados)."""
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
    hubs = {
        nodo: grado for nodo, grado in grados_subgrafo.items() if grado > promedio_grado
    }
    no_hubs = {
        nodo: grado
        for nodo, grado in grados_subgrafo.items()
        if grado <= promedio_grado
    }

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

    click.echo(
        f"Visualización de la red guardada como: visualizacion_{red_social}_hubs.png"
    )
    return True


def calcular_distancia_media(G):
    """Calcula la media de las distancias entre pares aleatorios de nodos en el grafo."""
    nodos = list(G.nodes())  # Obtener los nodos como una lista
    num_nodos = len(nodos)

    # Determinar el número de pares
    num_pares = 2000
    if num_nodos >= 2000:
        num_pares = 2000

    else:
        num_pares = num_nodos * (num_nodos - 1) // 2

    distancias = []

    if num_pares == 2000:
        # Seleccionar 2000 pares aleatorios si el grafo tiene suficientes nodos
        for _ in range(num_pares):
            nodo1, nodo2 = random.sample(nodos, 2)
            try:
                distancia = nx.shortest_path_length(G, source=nodo1, target=nodo2)
                distancias.append(distancia)
            except nx.NetworkXNoPath:
                # Ignorar los pares no conectados
                continue
    else:
        # Calcular todas las distancias si el número de pares es menor a 2000
        for i, nodo1 in enumerate(nodos):
            for nodo2 in nodos[i + 1 :]:
                try:
                    distancia = nx.shortest_path_length(G, source=nodo1, target=nodo2)
                    distancias.append(distancia)
                except nx.NetworkXNoPath:
                    # Ignorar los pares no conectados
                    continue

    if not distancias:
        return float("inf")  # Todos los nodos están desconectados

    solucion = sum(distancias) / len(distancias)

    click.echo(f"La distancia media es: {solucion}")
    return solucion


def bfs_distancia(grafo, origen):
    """Calcula la distancia más corta desde el nodo origen a todos los demás nodos utilizando BFS."""
    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[origen] = 0
    cola = deque([origen])

    while cola:
        nodo = cola.popleft()
        for vecino in grafo[nodo]:
            if distancias[vecino] == float("inf"):  # Si no se ha visitado
                distancias[vecino] = distancias[nodo] + 1
                cola.append(vecino)

    return distancias


def calcular_diametro(G):
    """Calcula y muestra el diámetro del grafo, que es la distancia más larga entre dos nodos cualesquiera, utilizando un muestreo si el grafo tiene más de 2000 nodos."""
    nodos = list(G.nodes())  # Obtener los nodos como una lista
    num_nodos = len(nodos)

    # Seleccionar un subconjunto de nodos si el grafo tiene más de 2000 nodos
    if num_nodos >= 2000:
        nodos_muestra = random.sample(nodos, 2000)  # Seleccionar 2000 nodos aleatorios
    else:
        nodos_muestra = nodos  # Usar todos los nodos si hay menos de 2000

    max_distancia = 0

    # Para cada nodo en el subconjunto, calculamos las distancias más cortas a todos los demás nodos
    for nodo in nodos_muestra:
        distancias = bfs_distancia(G, nodo)

        # Encontramos la distancia máxima desde este nodo
        distancia_maxima = max(
            distancia for distancia in distancias.values() if distancia != float("inf")
        )

        # Actualizamos el diámetro si encontramos una mayor distancia
        if distancia_maxima > max_distancia:
            max_distancia = distancia_maxima

    print(f"El diámetro de la red es: {max_distancia:.2f}")
    return max_distancia


def calcular_distancia_a_hubs(G, red_social):
    """Calcula la distribución de distancias desde los nodos a los hubs, considerando una muestra si el grafo tiene más de 2000 nodos."""
    if not os.path.isfile(f"distribucion_distancias_{red_social}_hubs.png"):

        # Obtener todos los nodos
        nodos = list(G.nodes())
        num_nodos = len(nodos)

        # Seleccionar nodos aleatorios si el grafo tiene 2000 o más nodos
        if num_nodos >= 2000:
            nodos = random.sample(nodos, 2000)

        # Identificar los hubs solo entre los nodos seleccionados
        grados = dict(
            G.degree(nodos)
        )  # Calcula el grado solo de los nodos seleccionados
        promedio_grado = sum(grados.values()) / len(grados)
        hubs = {nodo for nodo, grado in grados.items() if grado > promedio_grado}

        # Calcular las distancias más cortas desde cada nodo seleccionado a los hubs mediante bfs
        distancias_a_hubs = {}

        """for nodo in nodos:
            # Usamos el algoritmo de Dijkstra para encontrar la distancia más corta al nodo hub más cercano
            dist_min = min(nx.single_source_dijkstra_path_length(G, nodo).get(hub, float('inf')) for hub in hubs)
            distancias_a_hubs[nodo] = dist_min"""
        ##
        for i, nodo in enumerate(nodos):
            distancias = nx.single_source_shortest_path_length(G, nodo)
            dist_min = min(distancias.get(hub, float(1000)) for hub in hubs)
            if dist_min != 1000:
                distancias_a_hubs[nodo] = dist_min
        ##
        # Generar la distribución de distancias
        distribucion_distancias = {}
        for distancia in distancias_a_hubs.values():
            distribucion_distancias[distancia] = (
                distribucion_distancias.get(distancia, 0) + 1
            )

        # Mostrar la distribución de distancias en la consola
        for distancia, cantidad in distribucion_distancias.items():
            print(f"Distancia: {distancia:.2f}, Cantidad de Nodos: {cantidad}")

        click.echo(
            f"Distribución de distancias calculada y mostrada para la red {red_social}."
        )
        return distribucion_distancias
