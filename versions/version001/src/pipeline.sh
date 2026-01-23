#!/bin/zsh

### Go to Project Directory ###
dir='/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version001'
cd $dir || exit 1

### Activate Conda ###
source "$HOME/miniconda3/etc/profile.d/conda.sh" # initialize\
conda activate smoknet-env

### Pipeline ###

# >>> Process Data
F=src/001.py
in_dir=in/

echo -e "\n•••Running $F•••\n"
python $F --in_dir $in_dir --cwd $dir || exit 1
echo -e "\n•••$F Done•••\n"

# # >>> XXXX
# F=src/002.py
# echo -e "\n•••Running $F•••\n"
# python $F  || exit 1
# echo -e "\n•••$F Done•••\n"