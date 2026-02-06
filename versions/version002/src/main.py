
from src.functions import *
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
from pprint import pprint
import pygraphviz

os.chdir("/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version002")

in_dir = Path("in/simulated1")
out_dir = Path("out/main")
out_dir.mkdir(exist_ok=True)

# simulate reads
from src.simulate_reads import sim_reads

sim_reads(count = 1000, 
          len_range_lwr=25, 
          len_range_upr = 40, 
          seed = 100, 
          seq_len= 300,
          out_dir = str(in_dir))

fastas = load_data(in_dir)

QUERY = fastas['QUERY']
READS = fastas['READS']

_ , query = parse(QUERY) # len 1 list of single query
query = query[0] # str query
headers, sequences = parse(READS) # two lists




#\\\\
#\\\\
# Find Contigs
#\\\\
#\\\\
# # # use k as the some tail of read length distribution
# seq_summary = seq_summary(sequences) # read length stats
# pprint(seq_summary)
# k = seq_summary["Q3"].round().astype(int)
# counter = segment_all(sequences, k)
# # filter for frequent reads
# counter = Counter({k: v for k, v in counter.items() if v > 1})

query = 'dirtywetholefilledwiththeendsofwormsandanoozysmell'
txt = "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahobbitholeandthatmeanscomfort"
# txt = "XXXchristianandersonsitsachristiansdeskwritingalgorithmssdeskwritingalgorithms"
k = 9
counter = segment(txt, k)

len(counter)
kmer_lens = np.array([len(x) for x in counter])
pprint(summarize(kmer_lens))

# make adjacency matrix between each kmer
adj = make_adj(counter)

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

start = pd.Series([x[:k] for x in contigs]).value_counts().idxmax()
end = pd.Series([x[-k:] for x in contigs]).value_counts().idxmax()

max_length = max([len(x) for x in contigs])
longest = [contig for contig in contigs if contig[:k]==start and contig[-k:] == end and len(contig) > contig_summary["Q3"] ]

with open(out_dir/ "longest-contigs.txt", 'w') as f:
    for contig in longest:
        f.write(f"{contig}\n")


#\\\\
#\\\\
# Find Contigs
#\\\\
#\\\\
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

