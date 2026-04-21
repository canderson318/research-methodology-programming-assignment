import time
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
import subprocess as sp
from pathlib import Path


os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version003")
from src.functions import *


out_dir = Path("out/test2")
out_dir.mkdir(exist_ok=True)
in_dir = Path('in/test2')
in_dir.mkdir(exist_ok=True)


#\\\\
#\\\\
# Simulate strings from sentences
#\\\\
#\\\\
 
query = 'oundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsand'
txt = "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahobbitholeandthatmeanscomfort"


# # write random segments to fasta
# np.random.seed(210320) 
# with open(in_dir/"READS.fasta", 'wt', encoding = "UTF+8") as f:
#     for i in range(1000):
#         # lngth = np.random.choice(np.arange(5,10))
#         lngth = 10
#         strt = np.random.choice(range(len(txt)- lngth))
#         end = strt+lngth
#         f.write(f">{i}_sim:1234\n{txt[strt:end]}\n")

# write random segments to fasta
with open(in_dir/"READS.fasta", 'wt', encoding = "UTF+8") as f:
    lngth = 10
    for i in range(len(txt)-lngth):
        f.write(f">{i}_sim:1234\n{txt[i:(i+lngth)]}\n")

with open(in_dir / "QUERY.fasta", 'wt', encoding = "UTF+8") as f:
    f.write(f">QUERY\n{query}\n>>0_generative_seq:1234\n{txt}\n")

#\\\\
#\\\\
# Find Contigs
#\\\\
#\\\\
k = 5
t=1
save_adj = True; thresh = t; 

# Run
sp.run([
    './src/main.py',
    '--out_dir', out_dir,
    '--in_dir', in_dir,
    '-k', str(k),
    '--save_adjacency',
    '-t', str(t)
])


#\\\\
#\\\\
# Load results
#\\\\
#\\\\

q_contigs = np.loadtxt(out_dir/"ALLELES.fasta", dtype=str)
q_contigs = q_contigs[np.arange(len(q_contigs))%2 !=0] # contigs are odd items
print_contigs_with_context(q_contigs[:10], query, context=20)

adj = pd.read_csv(out_dir/"adjacency.csv", 
                  index_col = 0)
#\\\\
# Plot Graph
#\\\\

# fewest incomming edges
start = adj.sum(0).idxmin() # min colsums
# fewest outgoing edges
end = adj.sum(1).idxmin() # max rowsums

G = nx.from_pandas_adjacency(adj, create_using=nx.DiGraph)
node_colors = ["red" if n in start else "blue" if n in end else "None" for n in G.nodes()]

# pos = nx.spring_layout(G, seed=1048, method = 'energy', weight = None, k = 100)
# pos = nx.rescale_layout(pos, .2)
pos = nx.nx_agraph.graphviz_layout(G,prog = 'neato')
options = {"font_size": 15,"node_size": 1000,"node_color": node_colors,"edgecolors": None,"edge_color": "darkgrey","linewidths": 1,"width": 2}

fig = plt.figure(figsize = (30,30))
nx.draw(G,pos,with_labels=True,**options)
plt.savefig(out_dir/'graph.pdf')
plt.close()
