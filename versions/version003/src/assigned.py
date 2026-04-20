import networkx as nx
import matplotlib.pyplot as plt
import os
import subprocess as sp
from pathlib import Path


os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version002")
from src.functions import *


out_dir = Path("out/assigned")
out_dir.mkdir(exist_ok=True)
in_dir = Path('in/assigned')
in_dir.mkdir(exist_ok=True)

#\\\\
#\\\\
# Find Contigs
#\\\\
#\\\\

# k = 10 # odd for no palindrome
k = 32 # or 33
thresh = t = 3
sp.run([
    './src/main.py',
    '--out_dir', out_dir,
    '--in_dir', in_dir,
    '-k', str(k),
    '--save_adjacency',
    '-t', str(t)
], check = True)


#\\\\
#\\\\
# Load results
#\\\\
#\\\\
query = np.loadtxt(in_dir/"QUERY.fasta", dtype = str)[1]
contigs = np.loadtxt(out_dir/"contigs.txt", dtype=str)

try:
    q_contigs = np.loadtxt(out_dir/"query-contigs.txt", dtype=str)
    print_contigs_with_context(q_contigs, query, context=20)
except:
    print("No query contigs found.")

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
