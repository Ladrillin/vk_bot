import networkx as nx
import matplotlib.pyplot as mpl
import random

g = nx.Graph()

vertex_list = []
for i in range(0, 100):
    vertex_list.append(i)
g.add_nodes_from(vertex_list)

edge_list = []
for j in range(0, 100):
    edge_list.append((random.randint(0, j), random.randint(0, j)))

g.add_edges_from(edge_list)
nx.draw(g, with_labels=True)
mpl.savefig('test_graph_path_long_title.pdf')
mpl.show()
