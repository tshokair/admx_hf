"""
    main.py Author T. Shokair 9/11/15
    This main function reads in a list of power spectra, calls a function to process them, coadds each processed spectra, and finally plots a grand spectrum.
    
"""
import numpy as np
import random
from scipy import signal
import pylab as pl
import matplotlib.pyplot as plt
import time
from process_spectra import process
from pad_list import find_pad_param
from pad_list import pad_l
from noise_dist import single_bin_dev
#a file named p_spectra.txt should contain all of the runs to be included in a grand spectrum
runF=open("p_spectra.txt","r")
r_in=runF.readlines()
rn=list(map(int,r_in))
f0=[]
# lists to fill
p=[]
f=[]
wf=[]
wp=[]
n_ss=len(rn)
#Call functions to process data and fill lists
for i in range (0,n_ss):
    ls=process(rn[i])
    p.append(ls[1])
    f.append(ls[0])
    f0.append(ls[2])
    fs=ls[3]
    del ls
#pad each list so they can be added together
pad_param=find_pad_param(f,fs)
print(pad_param)
wp=[]
for i in range(0,n_ss):
    wp.append(pad_l(f[i],pad_param,p[i]))

wp_t=[a for a in wp[0]]
#sum the powers and offset the subspectra for plotting
sp=[]
sp.append([a+10 for a in p[0]])
for i in range (1,n_ss):
    sp.append([a+10*(i%8+1) for a in p[i]])
    wp_t=[a+b for a,b in zip(wp_t,wp[i])]
#create the full frequency list
f_t=np.linspace(pad_param[0],pad_param[1],pad_param[2])
#f_t=np.linspace(pad_param[0]+np.amin(f0)-.0008,pad_param[1]+np.amax(f0)+.0008,pad_param[2])
print(len(f_t[0:len(wp_t)]),len(wp_t))
print(f0)
#plot grand spectrum
plt.plot(f_t[0:len(wp_t)],wp_t)
#plot the individual subspectra
for i in range (0,n_ss):
    #print(len(f[i]),len(sp[i]))
    plt.plot(f[i][0:len(sp[i])],sp[i])
plt.ylabel('Power ')
plt.xlabel('Frequncy [GHz]')
plt.show()

#
# a template of the function is saved in noise_dist.py is called here, but this piece needs editing.
hist_pts=single_bin_dev(p)

n, bins, patches = pl.hist(hist_pts, 500, normed=1, histtype='stepfilled')
    
pl.yscale('log')
pl.ylabel('entries')
pl.xlabel('sigma')
pl.show()



