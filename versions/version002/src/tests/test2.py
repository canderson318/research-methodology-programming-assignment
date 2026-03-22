import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
from pprint import pprint
import pygraphviz


# raise NameError("need to fix how i ignore already seen reads. currently i return the contig if my next has been visited for simple cycle and branch that means i only explore the one path and not the branch as well\nadd repeat resolution where read locations are found based on alignment with main contigs")

os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version002")
from src.functions import *

# in_dir = Path("")
out_dir = Path("out/test2")
out_dir.mkdir(exist_ok=True)


#\\\\
#\\\\
#\\\\
#\\\\

# Run on sentence 
query = 'dirtywetholefilledwiththeendsofwormsandanoozysmell'
txt = "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahobbitholeandthatmeanscomfort"
k = 5
counter = segment(txt, k)

# make adjacency matrix between each kmer
adj = make_adj(counter)

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

#\\\
#\\\
# Find Contigs
#\\\
#\\\
contigs = make_contigs(adj)
print(f"{len(contigs)} contigs found")
contig_summary = summarize(np.array([len(x) for x in contigs]))
pprint(contig_summary)

with open(out_dir/ "contigs.txt", 'w') as f:
    for contig in contigs:
        f.write(f"{contig}\n")

candidate_sequences = [contig for contig in contigs if query in contig]
with open(out_dir/ "query-contigs.txt", 'w') as f:
    for contig in candidate_sequences:
        f.write(f"{contig}\n")


# start = pd.Series([x[:k] for x in contigs]).value_counts().idxmax()
# end = pd.Series([x[-k:] for x in contigs]).value_counts().idxmax()

max_length = max([len(x) for x in contigs])
longest = [contig for contig in contigs if contig[:k]==start and contig[-k:] == end and len(contig) > contig_summary["Q3"] ]

with open(out_dir/ "longest-contigs.txt", 'w') as f:
    for contig in longest:
        f.write(f"{contig}\n")


