
# 0.Import required modules
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import time


# edges = [("Lập", "Nhật"), ("Lập", "Trường"), ("Trường", "Hưng"), ("Trường", "Khánh"),
#     ("Tùng", "Khánh"), ("Huy", "Khánh"), ("Huy", "Tâm"), ("Tuấn", "Trường"), ("Tuấn", "Khánh"),
#     ("Rosé", "Trường"), ("Rosé", "Khánh")]

# 1.Create graph object
def create_edges():
        datafile = open('./popularity_weight.csv')
        edges = []
        for line in datafile:
            row_data = line.strip("\n").split(",")
            row_data = row_data[:2]
            
            # try:
            #     row_data[2] = float(row_data[2])
            # except ValueError:
            #     pass
            edges.append(row_data)
        edges.pop(0)
        return edges
    
def create_graph(edges):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph
  
# 2.Check if there is any node left with degree d
def check(graph_copy, d):
    is_choose = 0  # there is no node of deg <= d
    for i in graph_copy.nodes():
        if (graph_copy.degree(i) <= d):
            is_choose = 1
            break
    return is_choose
  
  
# 3.Find list of nodes with particular degree
def find_nodes(graph_copy, it):
    set1 = []
    for i in graph_copy.nodes():
        if (graph_copy.degree(i) <= it):
            set1.append(i)
    return set1

# 4.K shell decomposition
def k_shell_decomposition():
    graph = create_graph(create_edges())
    graph_copy = graph.copy()
    
    it = 1  
    tmp = [] # Bucket being filled currently
    buckets = [] # list of lists of buckets
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
def main():
    print(k_shell_decomposition())

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))

# 6.Visualization
# nx.draw(create_edges(), with_labels=1)
# plt.show()