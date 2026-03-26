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
    # print("\tFor > 2000 kmers, this can take a while") if counter.__len__() > 2000 else print("\tThis should not take too long.")
    t0 = time.time()
    contigs_res = make_contigs_from_adj(query = query, adj = adj)
    contigs = [contig for contig, _ in contigs_res]
    # which Kmers constructed contig
    contig_inds = [inds for _, inds in contigs_res] # each element contains the indices of the kmers used to create the contig in order
    t1 = time.time()
    dt =(t1 - t0)
    num_contigs = len(contig_inds)
    print(f"\tDone. {dt:.3f}s {num_contigs} contigs found\nE.g:")
    print_contigs_with_context(contigs[:min(5,num_contigs)], query, context=10)

    #++ ALLELES.fasta -> largest contig (allele) containing query
    
    #++ ALLELES.aln -> read, contig_id, location
    #++ ALLELES.tsv
    #++ - sseqid: read id from READS.fasta
    #++ - qseqid: contig id from ALLELES.fasta
    #++ - sstart: start of where read aligns with qseq (the largest matched contig)
    #++ - send: end of where read aligns with qseq (the largest matched contig)
    #++ - qstart: start of where contig aligns with sseq (the largest matched contig)
    #++ - qend: end of where contig aligns with sseq (the largest matched contig)
    #---> x, y, how x aligns with y, how y aligns with x

    
    #++ kmer_mapping ==> { 'kmer': [(read_index, (coordinates)), (other_read_index, (coordinates)),...], 'other_kmer':...
    # Kmer: the reads containing it and their coordinates in the read
    kmer_seq_coords = [coords  for x in kmer_mapping.values() for ind, coords in x] 
    kmer_read_ids = [ind  for x in kmer_mapping.values() for ind, coords in x ] # tuple of read indices for each kmer
    # Kmer: teh read IDs that contain it
    kmer_seq_ids = [headers[i] for i in kmer_read_ids ]
    
    kmers = []
    for key, values in kmer_mapping.items():
        kmers+= [key] * len(values)

    SystemExit("Fix the q/s start/end")

    # where read in contig 
    qstart = [pos * k for inds in contig_inds for pos in range(len(inds))]
    qend   = [pos * k + k for inds in contig_inds for pos in range(len(inds))]
    
    # kmer x read table (from kmer_mapping) 
    kmer_read_df = pd.DataFrame({
        'kmer_ind': [i for i, vals in enumerate(kmer_mapping.values()) for _ in vals],
        'kmer':  [key for key, vals in kmer_mapping.items() for _ in vals],
        'seqid': [headers[ind] for vals in kmer_mapping.values() for ind, _ in vals],
        'sstart':[s for vals in kmer_mapping.values() for _, (s, e) in vals],
        'send':  [e for vals in kmer_mapping.values() for _, (s, e) in vals],
    })

    # kmer x contig table (from contig_inds) 
    kmer_contig_df = pd.DataFrame({
        'kmer_ind':   [ind for inds in contig_inds for ind in inds],
        'qseqid':  [i   for i, inds in enumerate(contig_inds) for _ in inds],
        'qstart':qstart ,
        'qend':  qend    
    })

    # Write Data
    with open(out_dir / "ALLELES.fasta", 'wt') as f:
        for i,c in enumerate(contigs):
            f.write(f">{i}_contig\n{c}\n")
            
    # join and save
    (
        kmer_contig_df
        .merge(kmer_read_df, left_on='kmer_ind', right_index=True)
        .to_csv(out_dir/"ALLELES.tsv", sep = "\t", index = False)
    )
    
    (
        kmer_read_df
        .merge(kmer_contig_df, on='kmer_ind')
        .drop(columns='kmer_ind')
        .to_csv(out_dir/"ALLELES.aln", sep = "\t", index = False)
    )
    
    len(kmers)
    np.array(kmers)[contig_inds[0]]
    
    print("Saving...")
    
    print("Done")


if __name__ == "__main__":
    main()
