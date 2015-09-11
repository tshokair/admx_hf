"""
    noise_dist.py Author T. Shokair 9/11/15
    function takes in a series of power spectra, calculates the mean, and the deviations from the mean. returns single bin deviations as a histogram.
    
"""

import numpy as np
import random
from scipy import signal
import pylab as pl
import matplotlib.pyplot as plt
import pylab as P
import time
import math


def single_bin_dev(p):
    n_ss=len(p)
    p_av=[]
    hist_pts=[]
    binwidth=.01
    for i in range (0,n_ss):
        pts=len(p[i])
        p_av.append(sum(p[i])/len(p[i]))
        var=sum([(a-p_av[i])*(a-p_av[i]) for a in p[i]])/len(p[i])
        sig=math.sqrt(var)
        #print(p[i][0]-p_av[i])
        for j in range(0,pts):
            hist_pts.append((p[i][j]-p_av[i])/sig)
    return hist_pts







