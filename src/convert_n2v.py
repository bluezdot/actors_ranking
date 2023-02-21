import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

from sklearn.decomposition import PCA
from node2vec import Node2Vec as n2v
sns.set()

# def generate_graph_deg_dist(deg_dist, n):
#     '''
#     This function will generate a networkx graph G based on a degree distribution
#     provided by the user.
    
#     params:
#         deg_dist (Dictionary) : The key will be the degree and the value is the probability
#                                 of a node having that degree. The probabilities must sum to
#                                 1
#         n (Integer) : The number of nodes you want the graph to yield
                          
#     example:
#         G = generate_graph_deg_dist(
#                 deg_dist = {
#                     6:0.2,
#                     3:0.14,
#                     8:0.35,
#                     4:0.3,
#                     11:0.01
#                 },
#                 n = 1000
#         )
#     '''
#     deg = list(deg_dist.keys())
#     proba = list(deg_dist.values())
#     if sum(proba) == 1.:
#         deg_sequence = np.random.choice(
#             deg,
#             n,
#             proba
#         )
        
#         if sum(deg_sequence) % 2 != 0:
#             # to ensure that the degree sequence is always even for the configuration model
#             deg_sequence[1] = deg_sequence[1] + 1
        
#         return nx.configuration_model(deg_sequence)
#     raise ValueError("Probabilities do not equal to 1")
    
# G = generate_graph_deg_dist(
#         deg_dist = {
#             6:0.2,
#             3:0.14,
#             8:0.35,
#             4:0.3,
#             11:0.01
#         },
#         n = 5
# )

# 1. Process the data
def create_graph():
    
    def extract_from_file(file_path):

        buf = []

        with open(file_path, 'r') as f:
            while True:
                line = f.readline()

                if line == '':
                    break

                if line.startswith('ASIN: '):
                    buf.append({'ASIN': line.strip().split()[1]})
                elif line.strip().startswith('salesrank'):
                    buf[-1]['salesrank'] = int(line.strip().split()[-1])
                elif line.strip().startswith('similar'):
                    buf[-1]['similar'] = line.strip().split()[2:]

        return buf

    df = pd.DataFrame(extract_from_file('./data/amazon-meta.txt'))
    
    df = df[["ASIN", "similar"]]
    df = df[df['similar'].notna()]

    pairs = [[row.ASIN, node2] for row in df.itertuples() for node2 in row.similar]

    graph = nx.Graph()
    graph.add_edges_from(pairs)
    return graph

G = create_graph()

WINDOW = 1 # Node2Vec fit window
MIN_COUNT = 1 # Node2Vec min. count
BATCH_WORDS = 4 # Node2Vec batch words

g_emb = n2v(
  G,
  dimensions = 16,
  walk_length = 40, 
  num_walks = 5,
  workers = 2
)

mdl = g_emb.fit(
    vector_size = 16,
    window=WINDOW,
    min_count=MIN_COUNT,
    batch_words=BATCH_WORDS
)

dict1 = {}
for n in G.nodes():
    vector = mdl.wv.get_vector(str(n))
    dict[str(n)] = vector
  
# the json file where the output must be stored
out_file = open("/data/n2v_3.json", "w")
  
json.dump(dict1, out_file, indent = 6)
  
out_file.close()