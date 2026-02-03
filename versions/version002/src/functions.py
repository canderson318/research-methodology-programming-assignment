"""
Notes
- banded matrix where only query in region similar to query. 
- iterate until max hit when comparing s to s'

- de brujin graph for k mers comparing each suffix to every other prefix
- hamiltonian path to find contigs
- count kmer occurance with hash
- throw out infrequent kmers
"""

import numpy as np
import pandas as pd
from collections import Counter
import os
from pathlib import Path
import re
from numpy.typing import NDArray

def load_data(in_dir):
    """
    Read in fastas from `in_dir`
    
    :param in_dir: directory to fastas
    """
    
    print(f"Loading data from {in_dir}")
    
    files = os.listdir(Path(in_dir))
    fasta_files= [f for f in files if Path(f).match('*.fasta')]
    fasta_names = [Path(f).stem for f in fasta_files]

    if  "QUERY" not in fasta_names or  "READS" not in fasta_names:
        Exception(" No QUERY or READS file in `in_dir`")

    print(f"Loading: {', '.join(fasta_files)}...")

    fastas = {}
    for nm, file in zip(fasta_names, fasta_files):
        with open(f"{in_dir}/{file}", 'r') as f:
            lines =   f.readlines()
            fastas[nm] = [x for x in lines if  x.strip() and not x.lstrip().startswith("#")  ] # ignore commented

    print(f"Successfully Loaded: {', '.join(fastas.keys())}")

    return fastas


def parse(l:list) -> tuple:
    '''Process fasta list into headers and sequences'''
    # clean out newlines
    l = [s.strip("\n") for s in l]
    # make separate into headers and sequences
    headers = [s for s in l if re.match(">.+",str(s))] # where '>' prepends the list item
    sequences = [s for s in l if not re.match(">.+",str(s))] # where '>' doesn't prepend the list item
    return (headers, sequences)


def segment(s, t):
    """Return unique set of t length mers of s, and their frequency counts"""
    return [s[i:i+t] for i in range(len(s)-t+1)]


def segment_all(sequences:list, t):
    """Segment  all sequences and count tmers collectively"""
    return Counter(s[i:i+t]  for s in sequences for i in range(len(s)-1+t))


def summary(sequences):
    """Print Reads lengths stats"""
    def summarize(arr: NDArray):
        lngth = arr.shape[0]
        mu = np.mean(arr)
        sd = np.std(arr)
        med = np.median(arr)
        Q1 = np.quantile(arr, q = .25)
        Q2 = np.quantile(arr, q = .75)
        return {f"N":lngth, "mean":mu.round(3),"Q1":Q1.round(3),"Q2":Q2.round(3), "median": med.round(3), "sd": sd.round(3)}
    seq_lens = np.array([int(len(s)) for s in sequences])
    return summarize(seq_lens)


def align(s1,s2):
    """see if two same length strings match perfectly"""
    k = len(s1)
    ismatch = s1[1:k] == s2[0:(k-1)]
    return ismatch


def make_adj(counter):
    """Make an adjacency matrix between each combination from list of strings. fil matrix with (str1==str2) * average(counts)"""
    lngth = len(counter)
    mat = pd.DataFrame(np.zeros(lngth**2).reshape((lngth, lngth)), 
                       index = list(counter), columns = list(counter), 
                       dtype = float)
    for i in range(lngth):
        s1, v1 = list(counter.items())[i]
        for j in range(lngth):
            s2, v2 = list(counter.items())[j]
            if i != j:
                mat.iloc[i,j] = float(align(s1,s2)) * .5 * (v1+v2)
    return mat


def make_contigs(adj: pd.DataFrame):
    """Recursively search along adjacency matrix for contiguous strings"""
    indxs = adj.columns.to_numpy()
    adj_np = adj.to_numpy()
    # start nodes are those with th fewest incoming edges
    colsums = adj_np.sum(axis=0)
    starts = indxs[colsums == colsums.min()]
    contigs = []
    def dfs(curr, contig, visited):
        # values at current row
        row = adj_np[indxs == curr].ravel()
        # where edge with curr
        nexts = indxs[row > 0]
        # if end of string append contig and return nothing, exiting this function for that `start`
        if len(nexts) == 0:
            contigs.append(contig)
            return
        # for each connection
        for nxt in nexts:
            # if this hasnt been visited already skip rest of loop and go to another branch
            if visited[nxt] > 0:
                contigs.append(contig)
                continue
            new_visited = visited.copy()
            new_visited[nxt] += 1
            dfs(nxt,contig + nxt[-1],new_visited)
    for start in starts:
        dfs(start,start,Counter([start]))
    return contigs