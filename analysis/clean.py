import numpy as np
from scipy import stats
def remove_spikes(pw,fr,fs):
    peak_p=[]
    peak_f=[]
    peaks=[]
    #print(len(pw))
    for i in range(0,len(pw)):
        if i>6 and i<len(pw)-6:
            p_av=(np.average(pw[i-6:i-1])+np.average(pw[i+1:i+6]))/2
        elif i<6:
            p_av=np.average(pw[i+1:i+6])
        elif i>len(pw)-6:
            p_av=np.average(pw[i-6:i-1])
        if pw[i]>1.02*p_av:
            peaks.append(i)
            peak_f.append(fr[i])
            peak_p.append(pw[i])
#print(len(peaks))
    diff=[]
    for i in range(1,len(peaks)):
        df=(peaks[i]-peaks[i-1])*fs
        if df<.000032 and df>.000004:
            diff.append(df)
    pk_step=stats.mode(diff)[0][0]
    pk_ind=int(pk_step/fs)
    x=np.argwhere(fr==peak_f[20])[0][0]
    s_ind=x
    for i in range (0,50):
        if x-pk_ind*i>0:
            s_ind=x-pk_ind*i
        else:
            break

    j=s_ind
    for i in range(0,int((len(pw)-s_ind)/pk_ind)):
        p_sub=pw[j-5:j-2]+pw[j+2:j+5]
        for k in range (-2,3):
            pw[k+j]=np.average(p_sub)+np.random.normal()*np.std(p_sub)
        #pw[j]=(pw[j-1]+pw[j+1])/2
        j=j+pk_ind
#print(len(pw))
    return pw
