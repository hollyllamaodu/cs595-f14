#!/usr/bin/python

import json
import networkx as nx
from networkx.readwrite import json_graph

#open input directory
f = open('databefore.json')
nodes = json.load(f)
f.close()

#link the nodes from input
graph = json_graph.node_link_graph(nodes)

#call library
while nx.number_connected_components(graph) < 2:
    edges = nx.edge_betweenness_centrality(graph)
    Max = 0
    for edge in edges:
        if edges[edge] > Max:
            #iterate over it
            Max_edge = edge
            Max = edges[edge]            
    graph.remove_edge(Max_edge[0],Max_edge[1])

output = json_graph.node_link_data(graph)

g = open('dataAfter.json','w')
g.write(json.dumps(output))
g.close()