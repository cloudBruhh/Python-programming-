import matplotlib.pyplot as plt
import networkx as nx

# 1. Create an undirected graph
G = nx.Graph()

# 2. Add connections (Edges) between locations (Nodes)
# Each tuple represents a link: (Node1, Node2, weight/distance)
edges = [("A", "B", 4), ("B", "C", 3), ("A", "C", 8), ("C", "D", 2), ("B", "D", 6)]
G.add_weighted_edges_from(edges)

# 3. Analyze the graph properties
print(f"Total Nodes (Vertices): {G.number_of_nodes()}")
print(f"Total Edges (Links): {G.number_of_edges()}")

# 4. Find the shortest path using Dijkstra's Algorithm
shortest_path = nx.shortest_path(G, source="A", target="D", weight="weight")
path_length = nx.shortest_path_length(G, source="A", target="D", weight="weight")

print(f"\nShortest path from A to D: {' -> '.join(shortest_path)}")
print(f"Total path weight/distance: {path_length}")

# 5. Visualize the graph
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=1500,
    font_size=12,
    font_weight="bold",
)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.title("Simple Weighted Graph Visualization")
plt.show()
