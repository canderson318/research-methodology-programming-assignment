
import pandas as pd
import numpy as np
import os
from pathlib import Path
from numpy.typing import NDArray
import re
import pickle as pkl

wd = '/Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version001'
os.chdir(wd)
os.getcwd()

#\\\
#\\\
# Read in fastas
#\\\
#\\\

file = ''
print(f"Loading: {", ".join(file)}...")

print(f"Done")




# \\\
# \\\
# XXX XXX
# \\\
# \\\

# \\\
# \\\
# Save Data
# \\\
# \\\

# format output
out = 

# make out directory 
out_dir = Path('out/002')
out_dir.mkdir(exist_ok = True)
out_file = ''

print("Pickling Data...")
with open(out_dir / out_file, 'wb') as f:
    pkl.dump(out, f)
print("Done")

