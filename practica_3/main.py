import networkx as nx
import matplotlib.pyplot as plt

#esto es una prueba
#prueba2
#prueba3
#modifico algo

B = nx.Graph()

print("BITCOIN:")

with open ("bitcoin.edgelist", 'r') as f:
    aristasB = [tuple(map(int, line.strip().split())) for line in f]

B.add_edges_from(aristasB)

print("Numero de nodos: ", B.number_of_nodes())
print("Numero de aristas: ", B.number_of_edges())

grados = dict(B.degree())
# Promedio de grados
promedio_grado = sum(grados.values()) / len(grados)

#Antes de separar en hubs

'''distribucion_grados = {}
promedio = sum(grados.values()) / len(grados)
count = 0
for grado in grados.values():
    if grado > promedio:
        count +=1
    if grado in distribucion_grados:
        distribucion_grados[grado] += 1
    else :
        distribucion_grados[grado] = 1
        
        
print("Numero de nodos con un grado superior a la media (hubs): ", count)
max_value = max(distribucion_grados.keys())
plt.figure(figsize=(8,6))
#cambiar el ejex (keys) a valores log
plt.bar(distribucion_grados.keys(), distribucion_grados.values(), color = 'red')
# Personalización del gráfico
plt.xlabel("grados")
plt.ylabel("cantidad")
plt.title("distribucion de grados de los nodos")
plt.xlim([0, max_value])
plt.savefig("distribucion_bitcoinpng")
#print(max_value)
#print(grados)

# Cálculo del coeficiente de clustering
coef_clustering = nx.clustering(B)
# Agrupar los coeficientes de clustering en intervalos
coef_clustering_vals = list(coef_clustering.values())
clustering_bins = {}
for coef in coef_clustering_vals:
    bin = round(coef, 1)  # Agrupar en intervalos de 0.1
    if bin in clustering_bins:
        clustering_bins[bin] += 1
    else:
        clustering_bins[bin] = 1

# Ordenar los bins para graficar
clustering_bins = dict(sorted(clustering_bins.items()))

# Visualizar la distribución de coeficientes de clustering
plt.figure(figsize=(8, 6))
plt.bar(clustering_bins.keys(), clustering_bins.values(), color='blue', width=0.05)
plt.xlabel("Coeficiente de Clustering")
plt.ylabel("Cantidad de Nodos")
plt.title("Distribución del Coeficiente de Clustering")
plt.savefig("clustering_bitcoin.png")
'''

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
plt.savefig("distribucion_bitcoin_hubs.png")

# Cálculo del coeficiente de clustering
coef_clustering = nx.clustering(B)

# Identificar los coeficientes de clustering para hubs y no hubs
clustering_hubs = {nodo: coef for nodo, coef in coef_clustering.items() if nodo in hubs}
clustering_no_hubs = {nodo: coef for nodo, coef in coef_clustering.items() if nodo in no_hubs}

# Agrupar los coeficientes de clustering en intervalos
def agrupar_clustering(coeficientes):
    bins = {}
    for coef in coeficientes.values():
        bin = round(coef, 1)  # Agrupar en intervalos de 0.1
        bins[bin] = bins.get(bin, 0) + 1
    return bins

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
plt.savefig("clustering_bitcoin_hubs.png")


'''C = nx.DiGraph()

print("CONGRESS:")

with open ("congress.edgelist", 'r') as f:
    aristasC = [tuple(map(int, line.strip().split())) for line in f]

C.add_edges_from(aristasC)

print("Numero de nodos: ", C.number_of_nodes())
print("Numero de aristas: ", C.number_of_edges())

grados = dict(C.degree())

distribucion_grados = {}
promedio = sum(grados.values()) / len(grados)
count = 0
for grado in grados.values():
    if grado > promedio:
        count +=1
    if grado in distribucion_grados:
        distribucion_grados[grado] += 1
    else :
        distribucion_grados[grado] = 1
        
print("Numero de nodos con un grado superior a la media (hubs): ", count)
max_value = max(distribucion_grados.keys())
plt.figure(figsize=(8,6))
#cambiar el ejex (keys) a valores log
plt.bar(distribucion_grados.keys(), distribucion_grados.values(), color = 'red')
# Personalización del gráfico
plt.xlabel("grados")
plt.ylabel("cantidad")
plt.title("distribucion de grados de los nodos")
plt.xlim([0, max_value])
plt.savefig("distribucion.png")


F = nx.Graph()

with open ("facebook.edgelist", 'r') as f:
    aristasF = [tuple(map(int, line.strip().split())) for line in f]

F.add_edges_from(aristasF)

L = nx.Graph()

with open ("lastfm.edgelist", 'r') as f:
    aristasL = [tuple(map(int, line.strip().split())) for line in f]

L.add_edges_from(aristasL)'''

