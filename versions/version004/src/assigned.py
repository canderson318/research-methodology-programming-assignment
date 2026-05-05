import networkx as nx
import matplotlib.pyplot as plt
import os
import subprocess as sp
from pathlib import Path
import pickle as pkl

os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version004")
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
# k = 67 # or 33
k = 19
thresh = t = 3

sp.run([
    './src/main.py',
    '--out_dir', out_dir,
    '--in_dir', in_dir,
    '-k', str(k),
    '--save_adjacency',
    '-t', str(t)
], capture_output = False, check = True)



#\\\\
#\\\\
# ––– Plot grpah
#\\\\
#\\\\

fastas = load_data(in_dir)
READS = fastas['READS']
QUERY = fastas['QUERY']
_ , query = parse(QUERY)
_ , sequences = parse(READS)
query = query[0]

if False:
    res = []
    Ks = np.array(range(1,300,2))
    for k in Ks:
        res.append(len(segment_all(sequences, k)[0]))
    pkl.dump(res,open(out_dir/"k_count.pkl", 'wb'))
else:
    res = pkl.load(open(out_dir/"k_count.pkl", 'rb'))

xvals = np.arange(Ks.min(), Ks.max(), 1)
interpolated = np.interp(xvals, Ks, res)

_,ax = plt.subplots(figsize= (8,5))
ax.bar(xvals,interpolated.round(), zorder = 1, width = 1, alpha = .2, color = "#8043a3")
ax.scatter(xvals,interpolated.round(), s = 2, color ='#5a0d87', alpha = 1)
ax.set_xlabel("K")
ax.set_ylabel("Count")
ax.set_title("Relationship between K and count of unique K-mers")
peak_x = xvals[np.argmax(interpolated)]
peak_y = interpolated.max()
y_frac = peak_y / ax.get_ylim()[1]
ax.scatter(peak_x, peak_y, color='blue', marker='x')
ax.axvline(x=peak_x, ymax=y_frac, color='blue', linestyle='--', linewidth=1)
existing_ticks = [x for x in list(ax.get_xticks()) if x >= 0]
ax.set_xticks(existing_ticks + [peak_x])
tick_colors = ['black'] * len(existing_ticks) + ['blue']
for tick, color in zip(ax.xaxis.get_ticklabels(), tick_colors):
    tick.set_color(color)
ax.set_xlim((0,None))
plt.tight_layout()
plt.savefig(out_dir/"k_count.pdf")



q_contigs = np.loadtxt(out_dir/"ALLELES.fasta", dtype=str)
q_contigs = q_contigs[np.arange(len(q_contigs))%2 !=0] # contigs are odd items
# print_contigs_with_context(q_contigs[:10], query, context=100)

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
