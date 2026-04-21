from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
import subprocess as sp
from pathlib import Path
import pickle as pkl

os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version004")
from src.functions import *


out_dir = Path("out/test2")
out_dir.mkdir(exist_ok=True)
in_dir = Path('in/test2')
in_dir.mkdir(exist_ok=True)
os.listdir(out_dir)

#\\\\
#\\\\
# Simulate strings from sentences
#\\\\
#\\\\
 
query = 'obbitnotanast'
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

# write nonrandom segments to fasta
with open(in_dir/"READS.fasta", 'wt', encoding = "UTF+8") as f:
    lngth = 10
    for i in range(len(txt)-lngth):
        f.write(f">{i}_sim:1234\n{txt[i:(i+lngth+1)]}\n")

with open(in_dir / "QUERY.fasta", 'wt', encoding = "UTF+8") as f:
    f.write(f">QUERY\n{query}\n>>0_generative_seq:1234\n{txt}\n")

#\\\\
#\\\\
# Find Contigs
#\\\\
#\\\\
k = 5
t=0
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
