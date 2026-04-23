# src/tests/test_functions.py
import pytest
import sys
from pathlib import Path
import os
os.chdir(Path(__file__).parent.parent.parent)  # versions/version004/
from src.functions import *

def test_align_true():
    assert align("hat", "ath") == True

def test_align_false():
    assert align("hat", "xyz") == False

def test_segment_length():
    result = segment("ABCDE", 3)
    assert len(result) == 3  # ABC, BCD, CDE

def test_segment_keys():
    result = segment("ABCDEABC", 3)
    assert "ABC" in result
    assert result["ABC"] == [(0, 3), (5, 8)]
    assert "CDE" in result

def test_segment_all_counts():
    cntr, locs = segment_all(["ABCDE", "ABCDE"], 3)
    assert cntr["ABC"] == 2  # appears in both reads
    assert locs['ABC'] == [(0, [(0, 3)]), (1, [(0, 3)])] # at correct locations

def test_make_contigs():
    np.random.seed(42)
    query = 'GHIJK'
    txt = "ABCDEFGHIJKLMNOPQRSTUVWAXCGDFHG" 
    reads = []
    for i in range(200):
        lngth = np.random.choice(np.arange(5,15))
        strt = np.random.choice(range(len(txt)- lngth))
        end = strt+lngth
        reads.append(txt[strt:end])
    k = 3
    _, kmer_mapping = segment_all(reads, k)
    left_contigs, right_contigs, edge_list = make_contigs(kmer_mapping, query, k, max_visits = 5)
    left_joined_contigs = [ "".join(y if i == 0 else y[-1] for i, y in enumerate(x)) + query[k-1:] for x in left_contigs]
    right_joined_contigs = [query[:-k+1] + "".join(y if i == 0 else y[-1] for i, y in enumerate(x)) for x in right_contigs]
    n = 5
    top_left = np.argpartition([len(x) for x in left_joined_contigs], -min(n, len(left_joined_contigs)))[-n:]
    top_right = np.argpartition([len(x) for x in right_joined_contigs], -min(n,len(right_joined_contigs)))[-n:]
    full_contigs = [left_joined_contigs[li][:-len(query)] + right_joined_contigs[ri]for li in top_left for ri in top_right]
    largest_contig = max(full_contigs, key=len)
    # query in contig
    assert query in largest_contig, f"query {query!r} not found in contig {largest_contig!r}"
    # contig is a valid substring of the text
    assert largest_contig in txt, f"contig {largest_contig!r} not a substring of txt"
    # contig is longer than query
    assert len(largest_contig) > len(query), "contig should be longer than query alone"