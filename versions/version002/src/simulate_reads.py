
import numpy as np
from pathlib import Path
from numpy.random import Generator
from typing import Sequence, Tuple

def sim_reads(seed:int, seq_len:int, count:int, len_range_lwr:int, len_range_upr:int, out_dir:str):
    """Simulate Reads of specific length and count"""
    def generate(leng: int, lib:Sequence[str], rng: Generator) -> str:
        """Make random sequenc of basepairs"""
        seq = rng.choice(a = lib,   size=leng, replace = True)
        return "".join(seq)

    def chop(seq: str, length_range: Tuple[int,int], rng: Generator):
        """Chop up sequence into kmers with lengths in length_range """
        length = rng.integers(*length_range) # single int
        start = rng.integers(0, len(seq)-length + 1 ) # single int
        return seq[start:start+length]

    def make_reads(seq_len: int,count: int,len_range: Tuple[int, int],rng: Generator):
        """Yield reads and generator sequence"""
        seq = generate(seq_len, ["A", "T", "C", "G"], rng)
        def _reads():
            for _ in range(count):
                yield chop(seq, len_range, rng)

        return _reads(), seq


    # \\\
    # generate sequence and chop it up
    # \\\
    rng = np.random.default_rng(seed)
    rng = np.random.default_rng(seed)
    reads, gen_sequence = make_reads(seq_len = seq_len, count = count, len_range = (len_range_lwr,len_range_upr), rng = rng)
    
    # \\\
    # Save reads
    # \\\

    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)

    with open(out_dir/'READS.fasta', 'w', encoding = 'UTF8') as f:
        f.write(f">0_sim:1234\n")
        for i, read in enumerate(reads, start=1):
            f.write(f">{i}_sim:1234\n")
            f.write(f"{read}\n")

    with open(out_dir/'QUERY.fasta', 'w', encoding = 'UTF8') as f:
        f.write(f">QUERY\n{gen_sequence[10:30]}\n")
        f.write(f">0_generative_seq:1234\n{gen_sequence}\n")

