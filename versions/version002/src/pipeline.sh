#!/bin/zsh

### Go to Project Directory ###
dir='/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version001' # all paths relative to this
cd $dir || exit 1


### Pipeline ###

## >>>>>> Simulate Data >>>>>>
F=src/00.1-generate-reads.py
echo -e "\n•••Running $F•••\n"

conda run -n generic-python python $F \
--seq_len 150 \
--count 150 \
--len_range_lwr 10 \
--len_range_upr 20 \
--seed 10290 \
--out_dir 'in/test' \
|| exit 1

echo -e "\n•••$F Done•••\n"


## >>>>>> Process Data >>>>>>
F=src/001.py
echo -e "\n•••Running $F•••\n"

conda run -n generic-python python $F \
--cwd $dir \
--in_dir in/test/ \
--out_dir out/001/ \
--out_file query-with-reads.pkl \
|| exit 1

echo -e "\n•••$F Done•••\n"

# >>>>>> Find how each sequence aligns with every other >>>>>>
F=src.002
echo -e "\n•••Running $F•••\n"

conda run -n generic-python python -m $F  \
--cwd $dir \
--in_file out/001/query-with-reads.pkl \
--out_dir out/002 \
|| exit 1

echo -e "\n•••$F Done•••\n"


# >>>>>> Plot Graph >>>>>>
F=src/003.py
echo -e "\n•••Running $F•••\n"

conda run -n generic-python python $F  || exit 1

echo -e "\n•••$F Done•••\n"