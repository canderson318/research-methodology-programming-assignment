
import pandas as pd
import numpy as np
import os
from pathlib import Path
from numpy.typing import NDArray
import re
import pickle as pkl
import argparse

# os.getcwd()
# # '/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version001/src'

# \\\
# Load Data
# \\\

mat = pd.read_csv('../out/002/alignment-res.csv', index_col = 0)

rng = np.random.default_rng(123)
new_inds = rng.permutation(mat.shape[0])

mat = mat.iloc[new_inds, new_inds]

# \\\
# Make Graph 
# \\\

incoming = mat.sum(0)
start = incoming.idxmin()

order = [start]
visited = {start}

# while True:

#     # current node
#     curr = order[-1]

#     # outgoing edges from current
#     outgoing = mat.loc[curr]

#     # drop visited nodes
#     outgoing = outgoing.drop(visited)

#     # filter unconnectd nodes
#     outgoing = outgoing[outgoing>0]

#     if outgoing.empty:
#         break
    
#     # pick strongest overlap
#     nxt = outgoing.idxmax()
#     order.append(nxt)
#     visited.add(nxt)

## TRUTH
# AAATTTCCCGGG
# → TTTCCCGGGCGCG
# → CCCGGGCGCGATCGT
# → GGCGCGATCGTATCCGTA
# → GCGATCGTATCCGTATC

mat
