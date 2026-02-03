
import pandas as pd
import numpy as np
import os
from pathlib import Path
from numpy.typing import NDArray
import re
import pickle as pkl
import argparse

# local modules (rel to version00x); this script must be run as `python -m src.002`
from .alignment import alignment # function that finds how two strings align


def load_data(file):
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
    args = parser.parse_args()
    cwd = Path(args.cwd)
    in_file = args.in_file
    out_dir = cwd / args.out_dir

    # \\\
    # load data from 001
    # \\\
    query, sequences = load_data(cwd / in_file)

    # \\\
    # run on all sequences
    # \\\

    # make seq x seq matrix
    score_mat =  np.zeros([len(sequences), len(sequences)])
    shift_mat = score_mat.copy()

    # Return matrix of sequence alignment level with direction of alignment 
    #+ negative value means rows appear before columns, vice versa for positive values
    for i in range(score_mat.shape[0]):
        for j in range(score_mat.shape[1]):
            # grab strings
            s1, s2 = [sequences[z] for z in [i,j]]

            if s1 != s2: # don't self compare
                score, shift, direction= alignment(s1,s2)
                # print(alignment_summary(score, shift, direction))
                score_mat[i,j] = int(score)
                shift_mat[i,j] = int(shift*direction)
            
    score_mat = pd.DataFrame(score_mat, index = sequences, columns = sequences, dtype = int)
    shift_mat = pd.DataFrame(shift_mat, index = sequences, columns = sequences, dtype = int)

    # filter out negatives, this only saves one forward directional edges
    score_mat[shift_mat<0] = 0
    shift_mat[shift_mat<0] = 0
    


    # \\\
    # Save Data
    # \\\

    # set out directory
    Path(out_dir).mkdir(exist_ok = True)

    # format output
    out_dict = {'score': score_mat, "shift": shift_mat}

    for key, item in out_dict.items():
        out_file = key + ".csv"
        
        print(f"Saving Data: {out_dir / out_file} ...",)
        item.to_csv(out_dir /out_file , header = True, index = True)
        print("Done")


if __name__ == '__main__':
    main()

