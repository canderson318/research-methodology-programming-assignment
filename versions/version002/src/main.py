
from src.functions import *
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess as sp
from pathlib import Path
import re

os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version002")

Path("out/run").mkdir(exist_ok=True)

# simulate reads
from src.simulate_reads import sim_reads

sim_reads(count = 100, 
          len_range_lwr=10, 
          len_range_upr = 20, 
          seed = 100, 
          seq_len= 300,
          out_dir = 'in/simulated1/')

fastas = load_data('in/simulated1/')

QUERY = fastas['QUERY']
READS = fastas['READS']

_ , query = parse(QUERY) # len 1 list of single query
query = query[0] # str query
headers, sequences = parse(READS) # two lists


# txt = "InaholeinthegroundtherelivedahobbitNotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahobbitholeandthatmeanscomfort"
# counter = segment(txt)
seq_summary = summary(sequences) # read length stats

# use k as the lower tail of read length distribution
k = (seq_summary['median']-seq_summary['sd']).round().astype(int)
counter = segment_all(sequences, k)

# make adjacency matrix between each kmer
adj = make_adj(counter)

# G = nx.DiGraph()
# G.add_weighted_edges_from([
#         (i, j, adj.loc[i, j])
#         for i in adj.index
#         for j in adj.columns
#         if adj.loc[i, j] != 0
#     ])
G = nx.from_pandas_adjacency(adj, create_using=nx.DiGraph)
deg = dict(G.degree())
node_colors = ["red" if deg[n] > 2 else "lightgray" for n in G.nodes()]
pos = nx.spring_layout(G, seed=1048, method = 'energy', weight = None, k = 10)
options = {
    "font_size": 12,
    "node_size": 5000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 2,
    "width": 1,
    'node_color': node_colors
}

fig = plt.figure(figsize = (50,50))
nx.draw(G,pos,with_labels=True,**options)
plt.savefig('out/test/test.pdf')
plt.close()

contigs = make_contigs(adj)

query = "edahobbitNotanasty"

candidate_sequences = [contig for contig in contigs if query in contig]

