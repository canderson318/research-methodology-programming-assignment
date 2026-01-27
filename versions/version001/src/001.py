
import pandas as pd
import numpy as np
import os
from pathlib import Path
from numpy.typing import NDArray
import re
import pickle as pkl
import argparse


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
    '''
    Process fasta list into 
    headers
    sequences
    '''

    # clean out newlines
    l = [s.strip("\n") for s in l]

    # make separate into headers and sequences
    headers = [s for s in l if re.match(">.+",str(s))] # where '>' prepends the list item
    sequences = [s for s in l if not re.match(">.+",str(s))] # where '>' doesn't prepend the list item

    return (headers, sequences)


def print_summary(sequences):
    # how long is each read?
    def summary(arr: NDArray):
        lngth = arr.shape[0]
        mu = np.mean(arr)
        sd = np.std(arr)
        med = np.median(arr)
        Q1 = np.quantile(arr, q = .25)
        Q2 = np.quantile(arr, q = .75)
        print(f"N = {lngth}\nmean = {mu.round(3)} (Q1={Q1.round(3)},Q2={Q2.round(3)})\nmedian = {med.round(3)}\nsd = {sd.round(3)}")

    seq_lens = np.array([int(len(s)) for s in sequences])

    print()
    print("Read Lengths:")
    summary(seq_lens)
    print()


def main():

    #\\\
    # Parse Args
    #\\\
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", required = True, type = str)
    parser.add_argument("--in_dir", required = True, type = str)
    parser.add_argument("--out_dir", required = True, type = str)
    parser.add_argument("--out_file", required = True, type = str)

    args = parser.parse_args()

    cwd = Path(args.cwd)
    in_dir= cwd / Path(args.in_dir)
    out_dir = cwd / Path(args.out_dir)
    out_file =  Path(args.out_file)

    #\\\
    # Load Data
    #\\\
    
    fastas = load_data(in_dir)

    QUERY = fastas['QUERY']
    READS = fastas['READS']

    _ , query = parse(QUERY) # len 1 list of single query
    query = query[0] # str query
    headers, sequences = parse(READS) # two lists
    print_summary(sequences)

    #\\\
    # Save Data
    #\\\

    # format to dict
    out = {
        'query_str': query, 
        'reads': {
            'headers':headers, 
            'sequences':sequences
        } 
    }

    # make out directory
    out_dir.mkdir(exist_ok = True)

    print("Pickling Data...")
    with open(out_dir / out_file, 'wb') as f:
        pkl.dump(out, f)
    print("Done")

if __name__ == "__main__":
    main()

