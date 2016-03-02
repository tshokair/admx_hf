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
def process(rn,date,pm):
#rn=[201507310008]
#hf="/admx/admx-hf_data/testStandData/2015/07/31/"+str(rn)+".hdr"
#df="/admx/admx-hf_data/testStandData/2015/07/31/"+str(rn)+".psa"
    df="/mnt/nfs/admx/admx-hf_data/experimentData/"+date+"/"+rn+".psa"
    cf=(pm[0])
    pf=open(df)
    p_in=pf.readlines()
    p_s=list(map(float,p_in[1100:16100]))
    q=pm[1]
    f_dc=np.linspace(1100*pm[2],pm[2]*16100,len(p_s))
    dw=(f_dc[len(f_dc)-1]-f_dc[0])/2
    f=np.linspace(cf-dw,cf+dw,len(f_dc))
    #print(len(p_s),len(f))
    p=remove_spikes(p_s,f,pm[2])
    #print(len(p))
    #print(pm[2],f[0],f[len(f)-1])
    #p_av=fit(f,p,pm[0],pm[0]/pm[1])
    p_av=savgol_filter(p,2501,4)
    p_mean=np.average(p)
    """
    j=3
    for i in range(3,len(p)-3):
        p_av.append(np.average(p[j-3:j+3]))
        if (i-3)%6==0 and i>3:
            j=j+6
    """
    T=.5
    p_proc=[a/b-1 for a,b in zip(p,p_av)]
    del_s=calc_snr.delta_calc(p_proc,T,f,cf,cf/q,q)
    var_s=calc_snr.var_calc(p_proc,T,f,cf,cf/q,q)
    gamma=pm[0]/pm[1]
    wf=wf=[4*(a-0.0008)*(a-0.0008)/gamma/gamma for a in f]
    p_w=[a/(1+b) for a,b in zip(p_proc,wf)]
    return [f,p_w,cf,pm[2],p,p_proc,p_av,del_s,var_s]


"""
pw1=process(201508042777)
pw2=process(201507310008)
output_file("pspec.html")
#output_file("pspec_201507310008.html")
#output_file("pspec_201508042777.html")
p1 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Power")
p1.line(pw1[0],pw1[4],legend="201508042777")
p1.line(pw1[0],pw1[6],color="red",legend="Fit")

p2 = figure( x_axis_label="Frequency [GHz]",y_axis_label="Weighted Power")
p2.line(pw1[0],pw1[5],legend="201508042777")
#p2.line(pw2[0],pw2[5],color="red",legend="201507310008")

#p1.diamond(pk_f_new,pk_new,color="green")
#p1.square(peak_f,peak_p,color="black")
show(vplot(p1,p2))
"""
