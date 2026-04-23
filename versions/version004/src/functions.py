## notes:
# - build from both ends using k length substring of query
# - look at subgraph connected to query kmers
# - use coverage to weight
# - store only current previous and next

from ast import Dict, Tuple
import numpy as np
import pandas as pd
from collections import Counter
import os
from pathlib import Path
import re
from numpy.typing import NDArray
from collections import Counter
from typing import Dict, List, Tuple
import networkx as nx

def load_data(in_dir):
    """
    Read in fastas from `in_dir`
    :param in_dir: directory to fastas
    """
    
    files = os.listdir(Path(in_dir))
    fasta_files= [f for f in files if Path(f).match('*.fasta')]
    fasta_names = [Path(f).stem for f in fasta_files]

    if  "QUERY" not in fasta_names or  "READS" not in fasta_names:
        Exception(" No QUERY or READS file in `in_dir`")

    print(f"Loading: {in_dir}/[{', '.join(fasta_files)}]...")

    fastas = {}
    for nm, file in zip(fasta_names, fasta_files):
        with open(f"{in_dir}/{file}", 'r') as f:
            lines =   f.readlines()
            fastas[nm] = [x for x in lines if  x.strip() and not x.lstrip().startswith("#")  ] # ignore commented

    print(f"\tSuccessfully Loaded: {in_dir}/[{', '.join(fasta_files)}]")

    return fastas


def parse(l:list) -> tuple:
    '''Process fasta list into headers and sequences'''
    # clean out newlines
    l = [s.strip("\n") for s in l]
    # make separate into headers and sequences
    headers = [s for s in l if re.match(">.+",str(s))] # where '>' prepends 
    sequences = [s for s in l if not re.match(">.+",str(s))] # where '>' doesn't prepend
    return (headers, sequences)


def segment(s, t)-> Dict[str, Tuple[int,int]]:
    """Get all t-length strings and their locations in string"""
    result = {}                                                                                      
    for i in range(len(s) - t + 1):                                                                    
        kmer = s[i:i+t]
        if kmer not in result:                                                                         
            result[kmer] = []
        result[kmer].append((i, i+t))                                                                  
    return result

def segment_all(sequences: list[str], t: int) -> Tuple[Counter, Dict[str, List[int]]]:
    """Segment all sequences and count tmers collectively; save read index for each tmer"""
    cntr = Counter()
    read_ind = {}
    for i, s in enumerate(sequences):
        for tmer, loc in segment(s, t).items():
            cntr[tmer] += 1
            if tmer not in read_ind.keys():
                read_ind[tmer] = []
            # add tmer to read_ind dictionary as tuple -> (which_read, (start, stop))
            read_ind[tmer].append((i, loc))
    return cntr, read_ind

def summarize(arr: NDArray):
    lngth = arr.shape[0]
    mu = np.mean(arr)
    sd = np.std(arr)
    med = np.median(arr)
    Q1 = np.quantile(arr, q = .25)
    Q3 = np.quantile(arr, q = .75)
    return {f"N":lngth, "mean":mu.round(3),"Q1":Q1.round(3),"Q3":Q3.round(3), "median": med.round(3), "sd": sd.round(3)}

def seq_summary(sequences):
    """Print Reads lengths stats"""
    seq_lens = np.array([int(len(s)) for s in sequences])
    return summarize(seq_lens)


def align(s1,s2):
    """see if two same length strings match perfectly overlap s1[-1] == s2[-end]; for hat, cha -> lower diagonal = 0 (at != ch), upper diagonal = 1 (ha == ha)"""
    k = len(s1)
    # return s1[1:k] == s2[0:(k-1)]
    return s1[1:] == s2[:-1]

def make_contigs(kmer_mapping: Dict, query: str, k: int, max_visits: int = 2):
    """
    Build edge dict for the subgraph anchored on query k-mers, extended outward
    in both directions through read k-mers.

    max_visits: how many times a single path may traverse the same k-mer before
                stopping. 1 = classic visited-set behaviour. 2+ = allows passing
                through repeated k-mers (e.g. 'hole' in hobbit text) up to that
                many times before declaring a cycle.

    Returns: left_contigs, right_contigs, edge_list
    """
    
    keys = list(kmer_mapping.keys())
    query_keys = list(segment(query, k).keys())
    first, last = query_keys[0], query_keys[-1]

    def _connect(kmer: str, candidates: list, mapping_dict: Dict):
        """(prev_tuple|None, next_tuple|None, indices)"""
        if kmer not in candidates:
            return (None, None, mapping_dict.get(kmer, 0))
        whr_kmer = candidates.index(kmer)
        fwd_mask = np.array([align(kmer, x) for x in candidates])  # kmer -> x
        rev_mask = np.array([align(x, kmer) for x in candidates])  # x -> kmer
        fwd_mask[whr_kmer] = False
        rev_mask[whr_kmer] = False
        fwd = tuple(candidates[i] for i in np.where(fwd_mask)[0])
        rev = tuple(candidates[i] for i in np.where(rev_mask)[0])
        return (
            rev if rev_mask.any() else None,
            fwd if fwd_mask.any() else None,
            mapping_dict.get(kmer, 0),
        )

    edge_list = {}

    # Anchor every query k-mer into the read k-mer graph
    for kmer in query_keys:
        edge_list[kmer] = _connect(kmer, keys, kmer_mapping)

    # Traverse left: follow predecessors backward from first
    # visited is a count dict — stop a branch when any node hits max_visits
    to_explore = [(p, [p], {p: 1}) for p in (edge_list[first][0] or [])]
    left_contigs = []
    while to_explore:
        curr, contig, visited = to_explore.pop()
        if curr not in edge_list:
            edge_list[curr] = _connect(curr, keys, kmer_mapping)
        preds = edge_list[curr][0]
        if not preds:
            left_contigs.append(contig)
            continue
        for p in preds:
            count = visited.get(p, 0)
            if count >= max_visits:
                left_contigs.append(contig)  # cycle ->> save and stop branch
            else:
                to_explore.append((p, [p] + contig, {**visited, p: count + 1}))

    # Traverse right: follow successors forward from last
    to_explore = [(s, [s], {s: 1}) for s in (edge_list[last][1] or [])]
    right_contigs = []
    while to_explore:
        curr, contig, visited = to_explore.pop()
        if curr not in edge_list:
            edge_list[curr] = _connect(curr, keys, kmer_mapping)
        succs = edge_list[curr][1]
        if not succs:
            right_contigs.append(contig)
            continue
        for s in succs:
            count = visited.get(s, 0)
            if count >= max_visits:
                right_contigs.append(contig)  # cycle ->> save and stop branch
            else:
                to_explore.append((s, contig + [s], {**visited, s: count + 1}))

    return left_contigs, right_contigs, edge_list

def print_contig_with_context(contig, query, context):
    '''print string hilighting match with query'''
    BLUE = '\033[94m'
    RESET = '\033[0m'
    idx = contig.find(query)
    start = max(0, idx - context)
    end = min(len(contig), idx + len(query) + context)
    before = contig[start:idx]
    match = contig[idx:idx + len(query)]
    after = contig[idx + len(query):end]
    buff1 = '' if start == 0 else '...'
    buff2 = '' if end == len(contig) else '...'
    print(f"{buff1}{before}{BLUE}{match}{RESET}{after}{buff2}")

def print_contigs_with_context(contigs, query, context=10):
    for contig in contigs:
        print_contig_with_context(contig, query, context)
    

