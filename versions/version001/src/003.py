
import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess as sp
import re
import sys

np.random.seed(1203)
os.makedirs("out/003", exist_ok=True)

# read original sequence in from fasta
Q = [x.strip() for x in open('in/test2/QUERY.fasta', 'r').readlines()]

gen_header = next(i for i, x in enumerate(Q) if x.startswith(">0_generative")) # first index that satisfies condition

gen_seq = Q[gen_header+1]

# read matrices
score_df = pd.read_csv("out/002/score.csv")
shift_df = pd.read_csv("out/002/shift.csv")

if not all(score_df.columns == shift_df.columns):
    raise ValueError("Shift and Score dfs columns to not match.")

def process(df: pd.DataFrame, pmax_row,invert) -> np.ndarray:
    """
    - drop first column
    - max of duplicate rows/columns
    - keep only row-wise maxima
    """
    # drop rowname col
    df = df.iloc[:, 1:]
    # make rnames ununique again
    names = [re.sub(r"\.\d+$", "", x) for x in df.columns.values]
    # set these as col and index
    df.columns = names
    df.index = names
    # group by index, colmax, transpose groupby index (columns) colmax, transpose 
    df_avg = (df
        .groupby(level=0).max()
        .T.groupby(level=0).max()
        .T)
    # save colabels
    labels = df_avg.columns.values
    # make mat
    mat = df_avg.to_numpy(dtype=float)
    # take the inverse
    if invert:
        mat = np.linalg.inv(mat)
    # filter for just one edge per row
    if pmax_row:
        row_maxs = mat.max(axis=1, keepdims=True)
        mat[mat < row_maxs] = 0
    return mat, labels

score_mat, score_labels = process(score_df,pmax_row = True, invert = False)
shift_mat, shift_labels = process(shift_df, pmax_row  = True, invert = False)

# set shift to zero where score zero
shift_mat[score_mat==0] = 0


if not np.array_equal(score_labels, shift_labels):
    raise ValueError('Matrix labels do not match')

labels = score_labels

#\\\
#\\\
# construct graph
#\\\
#\\\
G = nx.DiGraph()

# add nodes with labels
G.add_nodes_from(labels)

# add score as edge weights and shifts as edge labels
label_dict = {}
for i, src in enumerate(labels):
    for j, tgt in enumerate(labels):
        w = score_mat[i, j]
        # shft = shift_mat[i, j]
        if w > 0:
            G.add_edge(src, tgt, weight=w)
            label_dict[(src,tgt)] = int(w)

# sum(label_dict.values())
# sys.exit("•••StopPoint•••")

# set labels
nx.set_edge_attributes(G,label_dict, 'label')

#\\\
#\\\
# Plot graph
#\\\
#\\\

print("Plotting...")
# align degres to nodes
degree = dict(G.degree())
degree_val = np.array([degree[n] for n in G.nodes()])

# scale degrees
quantiles = np.quantile(degree_val, np.linspace(0,1,10))
node_size = np.digitize(degree_val, quantiles, right = True)
node_size = (node_size**4) + 300

fig = plt.figure(figsize=(40, 40))
# pos = nx.spring_layout(G, seed=120349, method = 'energy')
pos = nx.spring_layout(G, seed=120349, method = 'force')
nx.draw_networkx_edge_labels(G, pos, font_size=10, edge_labels=nx.get_edge_attributes(G, "label") )
nx.draw(G, pos, with_labels=True, node_size=node_size, font_size=8)
ax = plt.gca()
ax.text(0.5,1,
    f"Original Sequence:\n{gen_seq}",
    transform=ax.transAxes,ha="center",va="bottom",fontsize=15)
plt.savefig("out/003/graph.pdf")
plt.close()

# sp.run(['open', 'out/003/graph.pdf', '-a', 'Preview'])


# #\\\
# # Random walks 
# #\\\

# rng = np.random.default_rng(1203)

# nodes = np.array(list(g.nodes))
# in_deg = np.array([g.in_degree(n) for n in nodes])
# start_nodes = nodes[in_deg < 2]

# paths = []

# for _ in range(100):
#     start = rng.choice(start_nodes)
#     walk = nx.random_walk(
#         g,
#         start,
#         length=g.number_of_nodes() - 1,
#         weight="weight"
#     )
#     paths.append(walk)

# paths = np.array(paths, dtype=object)

# # -----------------------------
# # Position extraction
# # -----------------------------

# sequences = score_df.columns[1:]
# z = {}

# for s in sequences:
#     locs = []
#     for path in paths:
#         hits = np.where(np.array(path) == s)[0]
#         if len(hits):
#             locs.extend(hits)
#     z[s] = np.array(locs)

# # -----------------------------
# # Rank + assemble dataframe
# # -----------------------------

# rows = []

# for nm, v in z.items():
#     if len(v) == 0:
#         continue
#     ranks = pd.Series(-v).rank().unique().astype(int)
#     for r in ranks:
#         rows.append({"seq": nm, "loc": r})

# d = pd.DataFrame(rows)

# # -----------------------------
# # Density plots (ggplot analogue)
# # -----------------------------

# g_plot = sns.FacetGrid(d, col="seq", col_wrap=4, sharex=False, sharey=False)
# g_plot.map_dataframe(sns.kdeplot, x="loc", fill=True, bw_adjust=3)

# plt.savefig("/tmp/tmp-plot.png", dpi=150)
# plt.close()

# os.system("open /tmp/tmp-plot.png")
