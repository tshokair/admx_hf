#for testing
import random
import calc_weights
import pad_list
import numpy as np
ll=[]
for i in range(0,3):
    ll.append([])
    for j in range (0,10):
        ll[i].append(3*i+j)
#print(ll)
pad_param=pad_list.find_pad_param(ll,1)

#print(pad_param)
var=[]
for i in range (0,3):
    var.append([])
    for j in range(0,10):
        var[i].append(random.random())
var_pad=[]
ll_pad=[]
for i in range (0,3):
    var_pad.append(pad_list.pad_l(pad_param[2],pad_param,var[i]))
    ll_pad.append(pad_list.pad_l(pad_param[2],pad_param,ll[i]))
#print(var_pad[i])
w_ijk=calc_weights.calc_weight_ijk(var_pad)
for i in range(0,3):
    print(len(w_ijk[i]))
    #print(np.transpose(w_ijk[i]))
print(np.transpose(w_ijk))
