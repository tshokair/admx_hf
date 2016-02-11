"""
    call_process_fn.py Author T. Shokair 2/10/16
    This function calls the processing functions on a list of
    files and returns the various processed and sorted streams 
    as a single list
    
"""
import numpy as np
from process_spectra import process
from sort_spec import sort_from_indexes
def call_process(f):
    runF=open(f,"r")
    #runF=open("p_spec_runs.txt","r")
    r_in=runF.readlines()
    rn=list(map(int,r_in))
    f0=[]
    # lists to fill
    p_uns=[]
    f_uns=[]
    f0_uns=[]
    fs_uns=[]
    del_uns=[]
    var_uns=[]
    wf=[]
    wp=[]
    n_ss=len(rn)
    #n_ss=25
    #Call functions to process data and fill lists
    for i in range (0,n_ss):
        print("Processing",rn[i])
        ls=process(rn[i])
        p_uns.append(ls[5])
        f0_uns.append(ls[2])
        f_uns.append(ls[0])
        fs_uns.append(ls[3])
        del_uns.append(ls[7])
        var_uns.append(ls[8])
        #print(len(ls[1]))
        del ls
    f_start=[item[0] for item in f_uns ]
    s_ind=np.argsort(f_start)
    f=sort_from_indexes(s_ind,f_uns)
    f=np.around(f,decimals=7)
    p=sort_from_indexes(s_ind,p_uns)
    f0=sort_from_indexes(s_ind,f0_uns)
    fs=sort_from_indexes(s_ind,fs_uns)
    del_s=sort_from_indexes(s_ind,del_uns)
    var_s=sort_from_indexes(s_ind,var_uns)
    return [f,p,f0,fs,del_s,var_s]
