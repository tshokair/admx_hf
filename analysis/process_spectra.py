import numpy as np
from read_header import read_head
import pylab as pl
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import stats
from bokeh.plotting import figure, show, output_file, vplot
from clean import remove_spikes
from fit_jpa import fit
import calc_snr
def rebin1(a, n):
    m = a.shape[0] // n   # // is synonym for floordiv()
    b = a[0:n*m]   # clip if needed
    return b.reshape((m,n)).sum(axis=1)
def process(rn,date,pm):
#rn=[201507310008]
    df="/mnt/nfs/admx/admx-hf_data/experimentData/"+date+"/"+rn+".psa"
    #hf="/Users/shokair1/axion/hf_data/"+str(rn)+".hdr"
    #df="/Users/shokair1/axion/hf_data/"+str(rn)+".psa"
    cf=(pm[0])
    print(df)
    pf=open(df)
    p_in=pf.readlines()
    p_s=list(map(float,p_in[1100:14601]))
    q=pm[1]
    f_dc=np.linspace(1.1E-3,14.6E-3,1351)
    dw=1.35E-3
    f=np.linspace(cf-dw/2,cf+dw/2,1351)
    #print(len(p_s),len(f))
   # p=remove_spikes(p_s,f,pm[2])
    p=[a for a in p_s]
    #print(len(p))
    #print(pm[2],f[0],f[len(f)-1])
    #p_av=fit(f,p,pm[0],pm[0]/pm[1])
    p_av=savgol_filter(p,601,2)
    p_mean=np.average(p)
    """
    j=3
    for i in range(3,len(p)-3):
        p_av.append(np.average(p[j-3:j+3]))
        if (i-3)%6==0 and i>3:
            j=j+6
    """
    T=.5
    p_proc_100Hz=np.array([a/b-1 for a,b in zip(p,p_av)])
    p_proc=rebin1(p_proc_100Hz,10)
    del_s=calc_snr.delta_calc(p_proc,T,f,cf,cf/q,q)
    var_s=calc_snr.var_calc(p_proc,T,f,cf,cf/q,q)
    gamma=pm[0]/pm[1]
    wf=wf=[4*(a-0.0008)*(a-0.0008)/gamma/gamma for a in f]
    p_w=[a/(1+b) for a,b in zip(p_proc,wf)]
    return [f,p_w,cf,pm[2]*10,p,p_proc,p_av,del_s,var_s]
"""
pw1=process("20160218_0_00000","20160218",[5.74842,13531.26,1E-7])
pw2=process("20160218_0_00001","20160218",[5.748385,13590.52,1E-7])
output_file("pspec.html")
#output_file("pspec_201507310008.html")
#output_file("pspec_201508042777.html")
p1 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Power")
p1.line(pw1[0],pw1[4],color="red",legend="Fit")
p2 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Filter Function")
p2.line(pw1[0],pw1[6],legend="201508042777")
p3 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Flattened Power")
p3.line(pw1[0],pw1[5],legend="201508042777")
p4 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Excess Signal")
p4.line(pw1[0],pw1[7],legend="201508042777")
p5 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Variance")
p5.line(pw1[0],pw1[8],legend="201508042777")
#p2.line(pw2[0],pw2[5],color="red",legend="201507310008")

#p1.diamond(pk_f_new,pk_new,color="green")
#p1.square(peak_f,peak_p,color="black")
show(vplot(p1,p2,p3,p4,p5))
"""
