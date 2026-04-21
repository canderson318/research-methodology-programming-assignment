
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import subprocess as sp

os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version003")
from src.functions import *


out_dir = Path("out/test3")
out_dir.mkdir(exist_ok=True)
in_dir = Path('in/test3')
in_dir.mkdir(exist_ok=True)

#\\\\
#\\\\
# Simulate reads
#\\\\
#\\\\
from src.simulate_reads import sim_reads

sim_reads(count = 1000, 
          len_range_lwr=25, 
          len_range_upr = 40, 
          seed = 100, 
          seq_len= 300,
          out_dir = str(in_dir))

fastas = load_data(in_dir)

READS, QUERY = fastas['READS'], fastas['QUERY']

_ , query = parse(QUERY) # len 1 list of single query
query = query[0] # str query
headers, sequences = parse(READS) # two lists




#\\\\
#\\\\
# Find Contigs
#\\\\
#\\\\

k = 8
sp.run([
    './src/main.py',
    '--out_dir', out_dir,
    '--in_dir', in_dir,
    '-k', str(k),
    '--save_adjacency'
])

contigs = np.loadtxt(out_dir/"contigs.txt", dtype=str)
adj = pd.read_csv(out_dir/"adjacency.csv", index_col = 0)

q_contigs = np.loadtxt(out_dir/"query-contigs.txt", dtype=str)
print_contigs_with_context(q_contigs, query, context=20)

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
