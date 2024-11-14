import networkx as nx
import matplotlib.pyplot as plt

#esto es una prueba
#prueba2
#prueba3

B = nx.DiGraph()

with open ("bitcoin.edgelist", 'r') as f:
    aristasB = [tuple(map(int, line.strip().split())) for line in f]

B.add_edges_from(aristasB)

#print(B.number_of_nodes())
#print(B.number_of_edges())

grados = dict(B.degree())

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
        
print(count)
max_value = max(distribucion_grados.keys())
plt.figure(figsize=(8,6))
#cambiar el ejex (keys) a valores log
plt.bar(distribucion_grados.keys(), distribucion_grados.values(), color = 'red')
# Personalización del gráfico
plt.xlabel("grados")
plt.xlim([0, max_value])
plt.ylabel("cantidad")
plt.title("distribucion de grados de los nodos")
plt.savefig("distribucion.png")
#print(max_value)
#print(grados)
'''C = nx.Graph()

with open ("congress.edgelist", 'r') as f:
    aristasC = [tuple(map(int, line.strip().split())) for line in f]

C.add_edges_from(aristasC)

F = nx.Graph()

with open ("facebook.edgelist", 'r') as f:
    aristasF = [tuple(map(int, line.strip().split())) for line in f]

F.add_edges_from(aristasF)

L = nx.Graph()

with open ("lastfm.edgelist", 'r') as f:
    aristasL = [tuple(map(int, line.strip().split())) for line in f]

L.add_edges_from(aristasL)'''

