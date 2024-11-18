
# Informe de Análisis de la Red Social

## Resumen
Este informe presenta el análisis de una red social representada en el archivo <_io.TextIOWrapper name='lastfm.edgelist' mode='r' encoding='UTF-8'>. A continuación se detallan las propiedades básicas de la red y visualizaciones de los resultados obtenidos.

### Propiedades Básicas de la Red
- **Número de nodos**: 100
- **Número de aristas**: 200

## Gráficos

### 1. Distribución de Grados de los Nodos
Este gráfico muestra la distribución de los grados de los nodos, con una distinción entre los nodos "hubs" (con mayor grado) y los "no hubs":

![Distribución de Grados](./distribucion_lastfm_hubs.png)

### 2. Distribución del Coeficiente de Clustering
El siguiente gráfico presenta la distribución del coeficiente de clustering, diferenciando entre los hubs y los nodos de menor grado:

![Coeficiente de Clustering](./clustering_lastfm_hubs.png)

### 3. Distribución Conjunta de Grados y Coeficiente de Clustering
Este gráfico muestra la distribución conjunta de los grados y los coeficientes de clustering, proporcionando una visión más detallada sobre la relación entre estas dos métricas en la red social:

![Distribución Conjunta](./distribucion_conjunta_lastfm.png)

## Conclusiones
A partir de los análisis anteriores, podemos extraer varias conclusiones:

- La red tiene 100 nodos y 200 aristas.
- La distribución de grados muestra una clara diferencia entre los nodos hubs y los nodos no hubs, lo que indica la existencia de una estructura de red jerárquica.
- La distribución del coeficiente de clustering indica que los hubs tienden a estar más conectados entre sí, formando comunidades más cohesionadas.
