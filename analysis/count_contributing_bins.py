import numpy as np
import math
def count_f_per_bin(f,f_start,f_stop,fs):
    n=math.ceil((f_stop+fs-f_start)/fs)
    f_per_bin=np.zeros(n)
    all_freq=np.linspace(f_start,f_stop,n)
    #print (all_freq)
    for i in range(0, len(all_freq)):
        for j in range(0, len(f)):
            if all_freq[i]>=f[j][0] and all_freq[i]<f[j][len(f[j])-1]:
                f_per_bin[i]+=1
#print(all_freq[i],"occurs",f_per_bin[i],"times")
    return f_per_bin
"""
#test
f=[[.1,.2,.3,.4,.5],[.3,.4,.5,.6,.7],[.0,.1,.2,.3,.4],[.4,.5,.6,.7,.8]]

print(count_f_per_bin(f,.0,.8,.1))
"""