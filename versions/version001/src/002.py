
import pandas as pd
import numpy as np
import os
from pathlib import Path
from numpy.typing import NDArray
import re
import pickle as pkl
import argparse

# local modules
os.chdir("src")
from alignment import alignment # function that finds how two strings align
os.chdir(".")


def load_data(file):
    print(">>>LoadingData")
    data = pkl.load(open(file, 'rb'))
    query = data['query_str']
    sequences = data['reads']['sequences']
    return query, sequences


def main():
    # \\\
    # parse args
    # \\\
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", required = True, type = str)
    parser.add_argument("--in_file", required = True, type = str)
    parser.add_argument("--out_dir", required = True, type = str)
    parser.add_argument("--out_file", required = True, type = str)
    args = parser.parse_args()
    cwd = Path(args.cwd)
    in_file = args.in_file
    out_dir = cwd / args.out_dir
    out_file = args.out_file

    # # \\\
    # # set i/o paths (NOT FOR BASH CALLING)
    # # \\\
    # cwd =  Path('/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version001')
    # in_file = 'out/001/query-with-reads.pkl' 
    # out_dir = cwd/'out/002'
    # out_file = 'alignment-res.csv'

    # \\\
    # load data from 001
    # \\\
    query, sequences = load_data(cwd / in_file)

    # \\\
    # run on all sequences
    # \\\

    # make seq x seq matrix
    mat = np.zeros([len(sequences), len(sequences)])

    # Return matrix of sequence alignment level with direction of alignment 
    #+ negative value means rows appear before columns, vice versa for positive values
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            # grab strings
            s1, s2 = [sequences[z] for z in [i,j]]

            if s1 != s2: # don't self compare
                score, shift, direction= alignment(s1,s2)
                # print(alignment_summary(score, shift, direction))
                mat[i,j] = int(score*direction)
            
    mat = pd.DataFrame(mat, index = sequences, columns = sequences, dtype = int)

    # filter out negatives, this only saves one forward directional edges
    mat[mat<0] = 0

    # \\\
    # Save Data
    # \\\

    # set out directory
    Path(out_dir).mkdir(exist_ok = True)

    # format output
    out = mat
    print(f"Saving Data: {out_dir / out_file}...",)
    out.to_csv(out_dir / out_file, header = True, index = True)
    print("Done")


if __name__ == '__main__':
    main()

