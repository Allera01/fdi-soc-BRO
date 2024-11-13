import networkx as nx
import matplotlib.pyplot as plt

B = nx.Graph()

with open ("bitcoin.edgelist", 'r') as f:
    aristasB = [tuple(map(int, line.strip().split())) for line in f]

B.add_edges_from(aristasB)

nx.draw(B, node_size = 10)
plt.savefig('grafobitcoin.png')

C = nx.Graph()

with open ("congress.edgelist", 'r') as f:
    aristasC = [tuple(map(int, line.strip().split())) for line in f]

C.add_edges_from(aristasC)

nx.draw(C, node_size = 10)
plt.savefig('grafocongress.png')

F = nx.Graph()

with open ("facebook.edgelist", 'r') as f:
    aristasF = [tuple(map(int, line.strip().split())) for line in f]

F.add_edges_from(aristasF)

nx.draw(F, node_size = 10)
plt.savefig('grafofacebook.png')

L = nx.Graph()

with open ("lastfm.edgelist", 'r') as f:
    aristasL = [tuple(map(int, line.strip().split())) for line in f]

L.add_edges_from(aristasL)

nx.draw(L, node_size = 10)
plt.savefig('grafolastfm.png')