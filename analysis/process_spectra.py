"""
   process_spectra.py Author T. Shokair 9/11/15
   function to read in a specific power spectrum file and return lists with real frequencies, weighted power, central frequency, and frequency steps.
   
"""
import numpy as np
from read_header import read_head
import pylab as pl
import matplotlib.pyplot as plt
def process(rn):
#rn=[201507310008]
    #edit path to data files
    #below are paths on Bk
    #hf="/admx/admx-hf_data/testStandData/2015/07/31/"+str(rn)+".hdr"
    #df="/admx/admx-hf_data/testStandData/2015/07/31/"+str(rn)+".psa"
    #below are paths on local machine
    hf="/Users/tshokair/Desktop/admxWork/data/07_31/"+str(rn)+".hdr"
    df="/Users/tshokair/Desktop/admxWork/data/07_31/"+str(rn)+".psa"
    pm=read_head(hf)
    cf=(pm[0])
    pf=open(df)
    p_in=pf.readlines()
    p=list(map(float,p_in[500:15500]))
    f=np.linspace(500*pm[2],pm[2]*15550,len(p))
    #print(pm[2],f[0],f[len(f)-1])
    p_av=[]
    p_mean=np.average(p)
    for i in range(3,len(p)-3):
        p_av.append(np.average(p[i-3:i+3]))
    p_proc=[a/b-p_mean for a,b in zip(p,p_av)]
    wf=wf=[4*(a-0.0008)*(a-0.0008)/pm[4]/pm[4] for a in f]
    p_w=[a/(1+b) for a,b in zip(p_proc,wf)]
    return [f,p_w,cf,pm[2]]

"""
p_w=process(201507310008)
plt.plot(p_w[0][3:len(p_w[0])-3],p_w[1])
plt.show()
ax.set_yscale("log", nonposy='clip')
"""