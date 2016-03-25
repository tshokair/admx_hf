"""
    main.py Author T. Shokair 9/11/15
    This main function reads in a list of power spectra, calls a function to process them, coadds each processed spectra, and finally plots a grand spectrum.
    updated 10/8/15 to fix some bugs with coadding and incorporate histogram plotting
    updated 2/10/16 to add snr spectra as well as to take some of the logic out of main and move it to separte programs.
    updated 2/27/16 by slewis to accept date input and feed input to shell script.
    updated 02/27/16 by slewis to accept date input and feed date to shell script, which generates the spectra list    
"""
import numpy as np
import random
import math
from scipy import signal
from scipy import optimize
from scipy.stats import norm
import pylab as pl
import matplotlib.pyplot as plt
import time
import subprocess
import subprocess # Used to call shell script

from pad_list import find_pad_param
from pad_list import pad_l
from six_bin_average import six_bin_av
import pickle
from fit_gauss import fit
from count_contributing_bins import count_f_per_bin

from calc_weights import calc_weight_ijk
from pad_list import find_pad_param
from pad_list import pad_l
from make_plots import plot_everything

from call_process_fn import call_process
class ReturnProcessedSorted(object):
    def __init__(self, f,p,f0,fs,delta_ij,sig_sq_ij):
        self.f = f
        self.f0 = f0
        self.fs = fs
        self.delta_ij =delta_ij
        self.sig_sq_ij = sig_sq_ij
        self.p = p
def processed_streams(l):
    return ReturnProcessedSorted(l[0],l[1],l[2],l[3],l[4],l[5])

# Get date. Only accepts inputs of the correct length and format which contain only numbers.
# Also checks to make sure there is a folder corresponding to the given date.
while True:
    try:
        date = int(input("Enter date (YYYYMMDD): "))
        if len(str(date)) != 8:
            print("This is not a complete date. Please use YYYYMMDD format.")
            continue
        else:
            # Call script to compile list of files
            try:
                subprocess.call(["./generateSpecList.sh", str(date)])
                break
            except:
                print("There is no data for this date. Please choose another date.")
    except ValueError:
        print("Invalid input. Date must be entered in YYYYMMDD format using only numbers.")

#get the processed streams
p_array=call_process("./p_spectra.txt",str(date))
f=processed_streams(p_array).f
f0=processed_streams(p_array).f0
fs=processed_streams(p_array).fs
p=processed_streams(p_array).p
sig_sq_ij=processed_streams(p_array).sig_sq_ij
delta_ij=processed_streams(p_array).delta_ij
n_ss=len(f)

#pad the streams with zeros for co-adding
print(len(fs))
pad_param=find_pad_param(f,fs[0])
p_pad=[]
delta_ij_pad=[]
sig_sq_ij_pad=[]
for i in range(0,n_ss):
    print(len(f[i]),len(p[i]))
    p_pad.append(pad_l(f[i],pad_param,p[i]))
    delta_ij_pad.append(pad_l(f[i],pad_param,delta_ij[i]))
    sig_sq_ij_pad.append(pad_l(f[i],pad_param,sig_sq_ij[i]))
#find the weighting factors
w_ijk=calc_weight_ijk(sig_sq_ij_pad)
w_ij=np.transpose(w_ijk)
#weight the delta_ij and sigma_sq_ij padded streams
delta_ij_pad_w=[]
sig_sq_ij_pad_w=[]
for k in range(0,n_ss):
    delta_ij_pad_w.append([a*b for a,b in zip(delta_ij_pad[k],w_ij[k])])
    sig_sq_ij_pad_w.append([a*b**2 for a,b in zip(sig_sq_ij_pad[k],w_ij[k])])
    
#sum the powers and offset the subspectra for plotting
#offset_snr are offset spectra, offset simply for plotting purposes.
normed_signal_c=[a/math.sqrt(b) if b!=0 else b for a,b in zip(delta_ij_pad_w[0],sig_sq_ij_pad_w[0])]
snr_c=[1/math.sqrt(b) if b!=0 else b for b in sig_sq_ij_pad_w[0]]
offset_snr=[]
offset_normed_sig=[]
offset=10
offset_snr.append([a+offset for a in snr_c])
offset_normed_sig.append([a+offset for a in normed_signal_c])
for i in range (1,n_ss):
    normed_signal=[a/math.sqrt(b) if b!=0 else b for a,b in zip(delta_ij_pad_w[i],sig_sq_ij_pad_w[i])]
    snr=[1/math.sqrt(b) if b!=0 else b for b in sig_sq_ij_pad_w[i]]
    offset_snr.append([a for a in snr])
    offset_normed_sig.append([a+offset*(i%40+1) for a in normed_signal])
    normed_signal_c=[a+b for a,b in zip(normed_signal_c,normed_signal)]
    snr_c=[a+b for a,b in zip(snr_c,snr)]
    del snr, normed_signal


#make the plots
plot_everything(n_ss,f,f0,snr_c,offset_snr,p,w_ij,normed_signal_c,offset_normed_sig,fs[0])
