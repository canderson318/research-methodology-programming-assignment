#!/Users/canderson/miniconda3/envs/res-meth/bin/python

import sys
from pathlib import Path
# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))
import argparse
try: 
    from functions import *
except: 
    raise ModuleNotFoundError

def parse_args():
    parser = argparse.ArgumentParser(
        prog='main',
        description='Find longest contiguous sequence containing a query from fasta reads.',
        usage='./main.py -k 10 --in_dir input/directory --out_dir output/directory --save_adjacency '
    )

    # file to read songs from
    parser.add_argument(
        '-i','--in_dir',
        type=str,
        default=None, 
        required = True,
        help='Directory to `READS` and `QUERY` fasta files.'
    )
    
    parser.add_argument(
        '-o','--out_dir',
        type=str,
        default=None, 
        required = True,
        help='Directory to direct output to.'
    )
    
    parser.add_argument(
        '-k',
        type=int,
        default=None, 
        required = True,
        help='Kmer sequence size.'
    )
    
    parser.add_argument(
        '-adj', '--save_adjacency',
        action='store_true',
        default=False, 
        required = False,
        help='Save Kmer adjacency matrix to `out_dir`.'
    )
    
    return parser.parse_args()

def main(): 
    
    args = parse_args()
    k = args.k
    save_adj = args.save_adjacency
    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    
    fastas = load_data(in_dir)

    READS , QUERY = fastas['READS'], fastas['QUERY']

    print("Processing reads...")
    _ , query = parse(QUERY) # len 1 list of single query
    query = query[0] # str query
    headers, sequences = parse(READS) # two lists

    # count kmers
    counter = segment_all(sequences, k)
    # filter for frequent reads
    counter = Counter({k: v for k, v in counter.items() if v > 1})

    # make adjacency matrix between each kmer
    adj = make_adj(counter)
    if save_adj:
        print("Saving adjacency...")
        adj.to_csv(out_dir/ "adjacency.csv")

    # Find Contigs
    print("Finding contigs...")
    contigs = make_contigs(adj)
    print(f"{len(contigs)} contigs found")
    print("Saving...")

    with open(out_dir/ "contigs.txt", 'w') as f:
        for contig in contigs:
            f.write(f"{contig}\n")

    candidate_sequences = [contig for contig in contigs if query in contig]
    with open(out_dir/ "query-contigs.txt", 'w') as f:
        for contig in candidate_sequences:
            f.write(f"{contig}\n")
    print("Done")


if __name__ == "__main__":
    main()
