"""
    pad_list.py Author T. Shokair 9/11/15
    takes in a set of frequncy lists and fins the min and max frequencies for coadding. returns each list padded with zeros so that coadding can occur
    
    """
import numpy as np
def find_pad_param(ll,fs):
    l_min=100000000
    l_max=0
    for i in range (0,len(ll)):
        if np.amax(ll[i])>l_max:
            l_max=np.amax(ll[i])
        if np.amin(ll[i])<l_min:
            l_min=np.amin(ll[i])
    #print(l_min,l_max)
    return [l_min,l_max,int((l_max-l_min)/fs),fs]

def pad_l(l,l_param,p):
    l_pad=[]
    if l[0]==l_param[0]:
        l_pad=np.lib.pad(p, (0,l_param[2]-len(l)), 'constant', constant_values=(0,0))
    elif l[len(l)-1]==l_param[1]:
        l_pad=np.lib.pad(p, (l_param[2]-len(l),0), 'constant', constant_values=(0,0))
    else:
        start_buff=int((l[0]-l_param[0])/l_param[3])
        end_buff=int((l_param[1]-l[len(l)-1])/l_param[3])
        print(start_buff,end_buff)
        print(l_param[1],l_param[2],len(l))
        l_pad=np.lib.pad(p, (start_buff,end_buff), 'constant', constant_values=(0,0))
    return l_pad
"""
ll=[[1,2,3,4,5],[2,3,4,5,6],[0,1,2,3,4]]
l_param=find_full_length(ll)
print(l_param)
print(pad(ll[0],l_param))
print(pad(ll[1],l_param))
print(pad(ll[2],l_param))
"""