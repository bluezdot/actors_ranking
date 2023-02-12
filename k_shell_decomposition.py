
# 0.Import required modules
import networkx as nx
import matplotlib.pyplot as plt

edges = [("Lập", "Nhật"), ("Lập", "Trường"), ("Trường", "Hưng"), ("Trường", "Khánh"),
    ("Tùng", "Khánh"), ("Huy", "Khánh"), ("Huy", "Tâm"), ("Tuấn", "Trường"), ("Tuấn", "Khánh")]

# 1.Create graph object
def create_graph(edges : list):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph
  
# 2.Check if there is any node left with degree d
def check(graph_copy, d):
    f = 0  # there is no node of deg <= d
    for i in graph_copy.nodes():
        if (graph_copy.degree(i) <= d):
            f = 1
            break
    return f
  
  
# 3.Find list of nodes with particular degree
def find_nodes(graph_copy, it):
    set1 = []
    for i in graph_copy.nodes():
        if (graph_copy.degree(i) <= it):
            set1.append(i)
    return set1


def k_shell_decomposition():
    graph = create_graph(edges)
    graph_copy = graph.copy()
    
    it = 1  
    # Bucket being filled currently
    tmp = []
    # list of lists of buckets
    buckets = []
    while (1):
        flag = check(graph_copy, it)
        if (flag == 0):
            it += 1
            buckets.append(tmp)
            tmp = []
        if (flag == 1):
            node_set = find_nodes(graph_copy, it)
            for each in node_set:
                graph_copy.remove_node(each)
                tmp.append(each)
        if (graph_copy.number_of_nodes() == 0):
            buckets.append(tmp)
            break
    return buckets

# 5.Get K Shell Decomposition
print(k_shell_decomposition())
  
# 6.Visualization
nx.draw(create_graph(edges), with_labels=1)
plt.show()