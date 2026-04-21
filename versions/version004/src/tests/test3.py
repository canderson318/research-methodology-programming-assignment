
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import subprocess as sp
import pickle as pkl
os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version004")
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

#\\\\
#\\\\
# ––– Plot grpah
#\\\\
#\\\\

q_contigs = np.loadtxt(out_dir/"ALLELES.fasta", dtype=str)
q_contigs = q_contigs[np.arange(len(q_contigs))%2 !=0] # contigs are odd items
print_contigs_with_context(q_contigs[:10], query, context=20)

edge_list = pkl.load(open(out_dir/"edge_list.pkl", 'rb'))

#\\\\
# Plot Graph
#\\\\
edge_list = [(key,x) 
             for key, val in edge_list.items() 
             if val[1] is not None
             for x in val[1]
             ]

G = nx.from_edgelist(edge_list)

pos = nx.nx_agraph.graphviz_layout(G,prog = 'neato')
options = {"font_size": 15,"node_size": 1000,"node_color": 'none',"edgecolors": 'none',"edge_color": "darkgrey","linewidths": 1,"width": 2}

fig = plt.figure(figsize = (30,30))
nx.draw(G,pos,with_labels=True,**options)
plt.savefig(out_dir/'graph.pdf')
plt.close()
