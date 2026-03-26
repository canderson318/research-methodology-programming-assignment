import numpy as np
from math import factorial
from decimal import Decimal, getcontext

def func(P, prec=50):
    pm2fac = factorial(P - 2)
    # Switch to high-precision e only when float64 would lose precision
    if pm2fac > 10**15:
        getcontext().prec = prec
        e = sum(Decimal(1) / Decimal(factorial(k)) for k in range(prec))
        return int(Decimal(pm2fac) * e)
    else:
        return int(pm2fac * np.e)

import math

for p in [10, 14758]:
    x = func(p)
    pow = int(math.log10(x))
    rem = x / 10**pow
    print(f"f({p}) = {rem:.2f}e{pow}")

# Ps = np.arange(3, 10, 1)
# paths = np.array([func(p) for p in Ps])

# fig, ax = plt.subplots(2,1, figsize = (8,4))
# ax[0].plot(Ps, paths)
# ax[0].set_title("Linear")
# plt.yscale("linear")
# ax[1].plot(Ps, paths)
# ax[1].set_title("Log")
# plt.yscale("log")
# plt.tight_layout()
# plt.show()
