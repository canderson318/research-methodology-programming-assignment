
import pandas as pd
import numpy as np
import os
from pathlib import Path
import re
import pickle as pkl
from numpy.typing import ArrayLike
from numpy.random import Generator
from typing import Sequence, Tuple
import argparse


def generate(leng: int, lib:Sequence[str], rng: Generator) -> str:
    """Make random sequenc of basepairs"""
    seq = rng.choice(a = lib,   size=leng, replace = True)
    return "".join(seq)


def chop(seq: str, length_range: Tuple[int,int], rng: Generator):
    """Chop up sequence into kmers with lengths in length_range """
    length = rng.integers(*length_range) # single int
    start = rng.integers(0, len(seq)-length + 1 ) # single int
    return seq[start:start+length]

# seq = generate(leng= int(100), lib =  ["A", "T", "C", "G"], seed = 10239)
# chop(seq, (20,80))
    
def make_reads(seq_len: int,count: int,len_range: Tuple[int, int],rng: Generator):
    """Yield reads and generator sequence"""
    seq = generate(seq_len, ["A", "T", "C", "G"], rng)
    def _reads():
        for _ in range(count):
            yield chop(seq, len_range, rng)

    return _reads(), seq

def main():

    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--seq_len", required = True, type = int, help = "Generative sequence basepair length")
    parser.add_argument("--count", required = True, type = int, help="Number of reads to generate")
    parser.add_argument("--len_range_lwr", required = True, type = int, help="Lower bound of read length")
    parser.add_argument("--len_range_upr", required = True, type = int, help="Upper bound of read length")
    parser.add_argument("--seed", required = True, type = int, help="RNG seed")
    parser.add_argument("--out_dir", required = True, type = str)

    args = parser.parse_args()

    # \\\
    # generate sequence and chop it up
    # \\\
    rng = np.random.default_rng(args.seed)
    reads, gen_sequence = make_reads(seq_len = args.seq_len, count = args.count, len_range = (args.len_range_lwr,args.len_range_upr), rng = rng)

    # \\\
    # Save reads
    # \\\

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)

    with open(out_dir/'READS.fasta', 'w', encoding = 'UTF8') as f:
        f.write(f">0_sim:1234\n")
        for i, read in enumerate(reads, start=1):
            f.write(f">{i}_sim:1234\n")
            f.write(f"{read}\n")

    with open(out_dir/'QUERY.fasta', 'w', encoding = 'UTF8') as f:
        f.write(f">QUERY\nAATTCCTTCC\n")
        f.write(f">0_generative_seq:1234\n{gen_sequence}\n")



if __name__ == "__main__":
    main()    