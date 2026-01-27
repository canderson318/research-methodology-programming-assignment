#!/bin/zsh

### Go to Project Directory ###
dir='/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version001' # all paths relative to this
cd $dir || exit 1

### Activate Conda ###
source "$HOME/miniconda3/etc/profile.d/conda.sh" # initialize\
conda activate generic-python

### Pipeline ###

## >>>>>> Process Data >>>>>>

F=src/001.py
echo -e "\n•••Running $F•••\n"

python $F \
--cwd $dir \
--in_dir in/test/ \
--out_dir out/001/ \
--out_file query-with-reads.pkl \
|| exit 1

echo -e "\n•••$F Done•••\n"

# >>>>>> Find how each sequence aligns with every other >>>>>>
F=src/002.py
echo -e "\n•••Running $F•••\n"

python $F  \
--cwd $dir \
--in_file out/001/query-with-reads.pkl \
--out_dir out/002 \
--out_file alignment-res.csv\
|| exit 1

echo -e "\n•••$F Done•••\n"