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
    return {s[i:i+t]: (i,i+t) for i in range(len(s)-t+1)}

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


def make_adj(counter:Counter):
    """Make an adjacency matrix between each combination from list of strings. fil matrix with (str1==str2) * average(counts)"""
    lngth = len(counter)
    keys = list(counter.keys())
    vals = list(counter.values())
    
    # mat = pd.DataFrame(np.zeros(lngth**2).reshape((lngth, lngth)), index = list(counter), columns = list(counter), dtype = float)
    
    # numpy for speed
    mat = np.zeros((lngth, lngth))

    for i in range(lngth):
        s1, v1 = keys[i], vals[i]
        for j in range(lngth):
            s2, v2 = keys[j], vals[j]
            if i != j:
                # fill with alignment * the average frequency of both
                mat[i,j] = float(align(s1,s2)) * .5 * (v1+v2)
    # return DF version
    return pd.DataFrame(mat, index=keys, columns=keys)


# def make_contigs_from_adj(adj: pd.DataFrame):
#     """Recursively search along adjacency matrix for contiguous strings"""
#     def _recurse(curr, contig, visited):

#         row = adj_np[indxs == curr].ravel()
#         nexts = indxs[row > 0]
#         # if terminal string, end contig else continue growing contig
#         if len(nexts) == 0:
#             contigs.append(contig)
#             return
        
#         # track if a branch grew
#         grew = False

#         # for each next add to contig if not see already, if seen already, return contig to contigs list
#         for nxt in nexts:
#             if nxt in visited: # if seen (cycle) stop writing to this contig
#                 contigs.append(contig)
#                 continue
#             grew = True
#             new_visited = visited | {nxt} # add to visited set
#             _recurse(nxt,contig + nxt[-1],new_visited)
        
#         # if no branches could be grew (all looped back (cycles)), save current contig 
#         ##++ (otherwise a branch may not be returned to contig list)
#         if not grew:
#             contigs.append(contig)

#     indxs = adj.columns.to_numpy()
#     adj_np = adj.to_numpy()

#     # start nodes are those with fewest incoming edges
#     colsums = adj_np.sum(axis=0)
#     starts = indxs[colsums == colsums.min()]
#     contigs = []
    
#     for start in starts:
#         _recurse(start,start,set({start}))
        
#     return contigs

# def make_contigs_from_adj(query:str, adj: pd.DataFrame):
#     """Recursively search along adjacency matrix for indices of contiguous strings"""
#     def _save_if_match(contig):
#         """add contig to contigs list if query string in current expanded branch"""
#         branch = "".join(str_index[contig])
#         if query in branch:
#             contigs.append(np.array(contig, dtype=np.int64))
            
#     def _recurse(curr, contig, visited): 
#         """recurse through graph saving array of int indices if query in string those indices specify"""
#         row = adj_np[indxs == curr].ravel()
#         nexts = indxs[row > 0]
#         # if terminal string, end contig else continue growing contig
#         if len(nexts) == 0:
#             _save_if_match(contig)
#             return
        
#         # track if a branch grew
#         grew = False

#         # for each next add to contig if not see already, if seen already, return contig to contigs list
#         for nxt in nexts:
#             if nxt in visited: # if seen (cycle) stop writing to this contig
#                 _save_if_match(contig)
#                 continue
#             grew = True
#             new_visited = visited | {nxt} # add to visited set
#             _recurse(nxt,contig+[nxt],new_visited)
        
#         # if no branches could be grew (all looped back (cycles)), save current contig 
#         ##++ (otherwise a branch may not be returned to contig list)
#         if not grew:
#             _save_if_match(contig)

#     str_index = adj.columns.values
#     indxs = np.arange(adj.shape[0],dtype= np.int32)
#     adj_np = (adj>0).to_numpy().astype(np.int8)

#     # start nodes are those with fewest incoming edges
#     colsums = adj_np.sum(axis=0)
#     starts = indxs[colsums == colsums.min()]
#     contigs = []
    
#     for start in starts:
#         _recurse(start,[start],set({start}))
        
#     return contigs

# def make_contigs_from_adj(query: str, adj: pd.DataFrame):
#     """Iteratively search along adjacency matrix for indices of contiguous strings"""
#     str_index = adj.columns.values
#     indxs = np.arange(adj.shape[0], dtype=np.int32)
#     adj_np = (adj > 0).to_numpy().astype(np.int8)
    
#     colsums = adj_np.sum(axis=0)
#     starts = indxs[colsums == colsums.min()]
#     contigs = []
    
#     def _save_if_match(contig):
#         """add contig to contigs list if query string in current expanded branch"""
#         string = "".join(str_index[np.array(contig)])
#         if query in string:
#             contigs.append(np.array(contig, dtype=np.int32))
    
#     for start in starts:
#         states = [(start, [start], {start})]  # (curr, contig, visited)
        
#         while states: # len(states) > 0
#             curr, contig, visited = states.pop()
#             row = adj_np[curr]
#             nexts = indxs[row > 0]
            
#             if len(nexts) == 0:
#                 _save_if_match(contig)
#                 continue
            
#             grew = False
#             for nxt in nexts:
#                 if nxt not in visited:
#                     grew = True
#                     states.append((nxt, contig + [nxt], visited | {nxt}))
#             if not grew:
#                 _save_if_match(contig)
#     return contigs

def construct_string_from_debrujin(kmers:NDArray, inds: NDArray):
    """Construct continuous string for debrujin graph path, appending every last character to string"""
    string = kmers[inds[0]] 
    for ind in inds[1:]:
        string+=kmers[ind][-1]
    return string

def make_contigs_from_adj(query: str, adj: pd.DataFrame)->list[tuple[str,NDArray[np.int32]]]:
    """Iteratively search along adjacency matrix for indices of contiguous strings"""

    def _get_starts(adj):
        col_sums = adj.sum(0)
        return np.argwhere(col_sums == col_sums.min()).ravel().astype(np.int32)
    def _get_nexts(curr):
        return np.argwhere(adj_np[curr, :] > 0).ravel().astype(np.int32)
    def _save(contig):
        """check if contig inds contain teh query string, if so save"""
        # append last char consecutively
        string = construct_string_from_debrujin(str_index, contig)
        if query in string:
            contig_arr = np.array(contig)
            contig_res.append((string,contig_arr))
    
    str_index = adj.columns.values
    adj_np = (adj > 0).to_numpy().astype(np.int8)
    starts = _get_starts(adj_np)
    contig_res = []

    for start in starts:
        
        states = [(start, [start], {start})]

        while states:
            # get current states
            current, contig, visited = states.pop() # take the last element of the list ( a tuple )
            nxts = _get_nexts(current)

            if len(nxts) == 0:
                _save(contig)
                continue

            for nxt in nxts:
                if nxt in visited:
                    _save(contig)
                    continue
                # update states pushing forward through tree
                #++ current:=nxt, contig:= contig+[nxt], visited:= visited + nxt
                #++ each item of states is a tuple encoding the [current, extending branch, and visited nodes]
                states.append((nxt, contig + [nxt], visited | {nxt}))  

    return contig_res


# def make_contigs_from_1D_array(query:str, kmers: NDArray, save_only_match = True):
#     inds = np.arange(len(kmers), dtype=np.int32)
#     contigs = set()  
#     def _save(contig, on_match):
#         string = "".join(kmers[np.array(list(contig))])
#         if (query in string and on_match) or not on_match:
#             contigs.add(contig)  
#     for start in inds:
#         state = [(start, (start,))]
#         while state:
#             curr, contig = state.pop()
#             visited = set(contig)
#             nxts = set(inds) - visited
#             grew = False
#             for nxt in nxts:
#                 if align(kmers[curr], kmers[nxt]):
#                     grew = True
#                     state.append((nxt, contig + (nxt,)))
#             if not grew:
#                 _save(contig, save_only_match)

#     return list(contigs)
# kmers = np.array(list(counter.keys()))
# C = make_contigs_from_1D_array(query, kmers, save_only_match = False)
# with open("/Users/canderson/Desktop/test.txt", 'wt') as f:
#     for inds in C:
#         f.write(f"{"".join(kmers[np.array(inds)])}\n")

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
    

