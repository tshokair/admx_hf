import numpy as np
def rebin1(a, n):
    m = a.shape[0] // n   # // is synonym for floordiv()
    b = a[0:n*m]   # clip if needed
    return b.reshape((m,n)).mean(axis=1)
def six_bin_av(p):
    pnp=np.array(p)
    return rebin1(pnp,6)
