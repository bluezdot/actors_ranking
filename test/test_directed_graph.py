import networkx as nx
import matplotlib.pyplot as plt

def directed_k_shell(G):
    # Initialize the k-shell decomposition
    k_shell = {}

    # Initialize the list of nodes in the k-shell
    nodes = list(G.nodes())

    # Initialize the list of nodes with zero degree
    zero_degree_nodes = []

    # Compute the in-degree and out-degree for each node
    in_degrees = {}
    out_degrees = {}
    for node in nodes:
        in_degrees[node] = sum([G[p][node].get('weight', 1) for p in list(G.predecessors(node))])
        out_degrees[node] = sum([G[node][s].get('weight', 1) for s in list(G.successors(node))])

    # Compute the minimum degree in the graph
    min_degree = min(list(in_degrees.values()) + list(out_degrees.values()))

    # Repeat the k-shell decomposition until all nodes have been assigned to a shell
    shell_num = 0
    while nodes:
        # Find the nodes with degree less than or equal to the current shell number
        shell_nodes = [n for n in nodes if in_degrees[n] + out_degrees[n] <= shell_num]

        # If there are no more shell nodes, increment the shell number and continue
        if not shell_nodes:
            shell_num += 1
            continue

        # Assign the shell number to the shell nodes
        for n in shell_nodes:
            k_shell[n] = shell_num

            # Remove the node from the list of nodes and its in- and out-edges from the graph
            nodes.remove(n)
            zero_degree_nodes.append(n)
            for neighbor in list(G.neighbors(n)):
                if neighbor not in zero_degree_nodes:
                    in_degrees[neighbor] -= G[n][neighbor].get('weight', 1)
                    out_degrees[neighbor] -= G[n][neighbor].get('weight', 1)

    return k_shell


# Create a directed graph
G = nx.DiGraph()
edges = [("Lập", "Nhật"), ("Lập", "Trường"), ("Trường", "Hưng"), ("Trường", "Khánh"),
    ("Tùng", "Khánh"), ("Huy", "Khánh"), ("Huy", "Tâm"), ("Tuấn", "Trường"), ("Tuấn", "Khánh"),
    ("Rosé", "Trường"), ("Rosé", "Khánh")]
# edges = [(1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (3, 2), (3, 4), (4, 1)]
G.add_edges_from(edges)

# Compute the k-shell decomposition
k_shell = directed_k_shell(G)
print(k_shell)

# Visualize the graph with k-shell colors
pos = nx.circular_layout(G)
node_colors = [k_shell[node] for node in G.nodes()]
node_sizes = [100 * (k_shell[node] + 1) for node in G.nodes()]
nx.draw_networkx(G, pos, node_color=node_colors, node_size=node_sizes, cmap=plt.cm.Blues)
plt.axis('off')
plt.show()
