#!/Users/canderson/miniconda3/envs/res-meth/bin/python

import sys
from pathlib import Path
import time
from pprint import pprint
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
        usage='./main.py -k 10 --in_dir input/directory --out_dir output/directory --save_adjacency -t 10'
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
    
    parser.add_argument(
        '-t', '--filter_threshold',
        type = int,
        default=1, 
        required = False,
        help='Filter out kmers with frequency below this value.'
    )
    
    return parser.parse_args()

def main(): 
    
    args = parse_args()
    k = args.k
    thresh = args.filter_threshold
    save_adj = args.save_adjacency
    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    
    # load data
    fastas = load_data(in_dir)
    READS , QUERY = fastas['READS'], fastas['QUERY']

    print("Processing reads...")
    print("\tparsing reads...")
    _ , query = parse(QUERY) # len 1 list of single query
    query = query[0] # str query
    headers, sequences = parse(READS) # two lists

    print("***Reads Summary***")
    pprint(seq_summary(sequences))

    # count kmers
    print("\tsegmenting reads and counting kmers...")
    counter, kmer_mapping = segment_all(sequences, k)
    print(f"\t\t{counter.__len__():,} unique {k}-mers from {len(sequences):,} total reads")
    
    # filter for frequent reads
    print(f"\tfiltering for kmer frequency > {thresh}...")
    counter = Counter({k: v for k, v in counter.items() if v > thresh})
    kmer_mapping = {kmer:value for kmer,value in kmer_mapping.items() if kmer in counter}
    print(f"\t\t{counter.__len__():,} unique {k}-mers after filtering")
    
    if counter.__len__() == 0:
        raise ValueError(f"\n\tNo unique {k}-mers with frequency > {thresh}")
    

    # make adjacency matrix between each kmer
    print("\tmaking adjacency matrix...")
    t0 = time.time()
    adj = make_adj(counter)
    t1 = time.time()
    dt =(t1 - t0)
    print(f"\t\t{dt:.0f} s")
    
    if save_adj:
        print("\tSaving adjacency...")
        adj.to_csv(out_dir/ "adjacency.csv", index=True)

    # Find Contigs
    print("Finding contigs...")
    print("\tFor > 2000 kmers, this can take a while") if counter.__len__() > 2000 else print("\tThis should not take too long.")
    t0 = time.time()
    contigs = make_contigs_from_adj(query, adj)
    t1 = time.time()
    dt =(t1 - t0)
    print(f"\t{dt:.3f} s\n\t{len(contigs)} contigs found")
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
