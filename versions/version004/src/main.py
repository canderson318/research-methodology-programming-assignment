#!/Users/canderson/miniconda3/envs/res-meth/bin/python

import sys
from pathlib import Path
import time
import pickle as pkl
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

    #\\\\
    #\\\\
    # ––– Parse Args
    #\\\\
    #\\\\
    args = parse_args()
    k = args.k
    thresh = args.filter_threshold
    save_adj = args.save_adjacency
    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)


    #\\\\
    #\\\\
    # ––– Load Data
    #\\\\
    #\\\\
    fastas = load_data(in_dir)
    READS , QUERY = fastas['READS'], fastas['QUERY']

    print("Processing reads...")
    print("\tparsing reads...")
    _ , query = parse(QUERY) # len 1 list of single query
    query = query[0] # str query
    headers, sequences = parse(READS) # two lists

    print("***Reads Summary***")
    pprint(seq_summary(sequences))

    #\\\\
    #\\\\
    # ––– Count Kmers
    #\\\\
    #\\\\
    print("\tsegmenting reads and counting kmers...")
    counter, kmer_mapping = segment_all(sequences, k)
    print(f"\t\t{counter.__len__():,} unique {k}-mers from {len(sequences):,} total reads")

    # whr = np.argwhere([x.find("ort")!=-1  for x in counter.keys()]).ravel()
    # np.array([x for x in counter.keys()] )[whr]
    
    #\\\\
    #\\\\
    # ––– Filter for frequent reads
    #\\\\
    #\\\\
    print(f"\tfiltering for kmer frequency > {thresh}...")
    counter = Counter({k: v for k, v in counter.items() if v > thresh})
    kmer_mapping = {kmer:value for kmer,value in kmer_mapping.items() if kmer in counter}
    print(f"\t\t{counter.__len__():,} unique {k}-mers after filtering")

    if counter.__len__() == 0:
        raise ValueError(f"\n\tNo unique {k}-mers with frequency > {thresh}")

    #\\\\
    #\\\\
    # ––– Make edge list
    #\\\\
    #\\\\
    print("\tmaking edge list and finding contigs...")
    t0 = time.time()
    left_contigs, right_contigs, edge_list = make_contigs(kmer_mapping, query, k,max_visits = 2)
    t1 = time.time()
    dt =(t1 - t0)
    print(f"\t\t{dt:.0f} s")

    if save_adj:
        print("\tSaving edge list...")
        pkl.dump(edge_list, open(out_dir/ "edge_list.pkl",'wb'))

    all_contigs = left_contigs + right_contigs # list of lists of kmers that make up each contig

    # combnine each contig list to one string, append query at correct end/beginning for left/right contigs
    left_joined_contigs = [
      "".join(y if i == 0 else y[-1] for i, y in enumerate(x)) + query[k-1:]
      for x in left_contigs
    ]
    right_joined_contigs = [
      query[:-k+1] + "".join(y if i == 0 else y[-1] for i, y in enumerate(x))
      for x in right_contigs
    ]
    all_joined_contigs = left_joined_contigs + right_joined_contigs

    n = 5  # top N from each side
    top_left = np.argpartition([len(x) for x in left_joined_contigs], -min(n, len(left_joined_contigs)))[-n:]
    top_right = np.argpartition([len(x) for x in right_joined_contigs], -min(n,len(right_joined_contigs)))[-n:]

    full_contigs = [
        left_joined_contigs[li][:-len(query)] + right_joined_contigs[ri]
        for li in top_left for ri in top_right
    ]

    largest_contigs = {f"contig{i}": x for i,x in enumerate(full_contigs)}
    
    largest_contig = largest_contigs.get("contig0")
    print_contig_with_context( largest_contig, query, context = 1000)

    # overwrite with just the largest
    largest_contigs = {'contig0': largest_contig}

    #\\\\
    #\\\\
    #\\\\
    #\\\\
    # ––– Make Outputs
    #\\\\
    #\\\\
    #\\\\
    #\\\\
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

    #\\\\
    #\\\\
    # ––– ALLELES.fasta
    #\\\\
    #\\\\
    with open(out_dir / "ALLELES.fasta", "w") as f:
        for key,val in largest_contigs.items():
            f.write(f">{key}\n")
            f.write(val + "\n")

        
        
        
    #\\\\
    #\\\\
    # ––– ALLELES.aln
    #\\\\
    #\\\\
    #+ map reads to contigs
    #++ first: map contig kmers to contig
    #++ second: look up read kmer in contig_kmer_mapping
    #++ third: convert kmer loc in contig to contig overlap with read rooted at kmer
    
    rows = []
    # contig_id = 'contig0'; contig = largest_contigs.get(contig_id) ; header = headers[0]; read = sequences[0]
    for contig_id, contig in largest_contigs.items():
        # build kmer: [positions in this contig] once per contig
        contig_kmer_pos = {}
        for i in range(len(contig) - k + 1): # for each k-length mer
            kmer = contig[i:i+k]
            if kmer not in contig_kmer_pos:
                contig_kmer_pos[kmer] = []
            contig_kmer_pos[kmer].append(i)

        for header, read in zip(headers, sequences):
            offsets = []
            for j in range(len(read) - k + 1):
                kmer = read[j:j+k]
                if kmer in contig_kmer_pos:
                    for contig_i in contig_kmer_pos[kmer]:
                        offsets.append(contig_i - j)
            if not offsets:
                continue
            offset = Counter(offsets).most_common(1)[0][0]
            qstart = max(0, offset)
            qend   = min(len(contig), offset + len(read))
            sstart = qstart - offset
            send   = sstart + (qend - qstart)
            if read[sstart:send]  != contig[qstart:qend]: # stop if alignment not right
                continue
            rows.append({
                "sseqid": header.removeprefix('>'),
                "qseqid": contig_id,
                "sstart": sstart,
                "send":   send,
                "qstart": qstart,
                "qend":   qend,
            })

    alleles_aln = pd.DataFrame(rows).drop_duplicates(subset=["sseqid", "qseqid"])
    alleles_aln = alleles_aln.reset_index(drop=True)  # after drop_duplicates
    
    def check_alleles_aln(alleles_aln):
        """Check that sseq at start/end == qseq at start/end for all matches"""
        res = []
        for i in range(alleles_aln.shape[0]):
            row = alleles_aln.iloc[i]
            read_sub   = sequences[headers.index(f">{row['sseqid']}")][row['sstart']: row['send']]
            contig_sub = largest_contigs.get(row['qseqid'])[row['qstart']: row['qend']]
            res.append(read_sub == contig_sub)

        if np.sum(~np.array(res)):
            raise ValueError("alleles_aln has some incorrect alignment.")

    check_alleles_aln(alleles_aln)
    
    
    #\\\\
    #\\\\
    # ––– SAVE RESULTS
    #\\\\
    #\\\\
    print("Saving...")
    alleles_aln.to_csv(out_dir / "ALLELES.tsv", sep="\t", index=False)
    print("Done")


if __name__ == "__main__":
    main()
