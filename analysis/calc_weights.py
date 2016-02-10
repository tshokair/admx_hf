import numpy as np
def calc_weight_ij(var):
    sum_var=np.sum(var)
    w_ij=[]
    for vi in var:
        if vi==0:
            w_ij.append(0)
        else:
            w_ij.append(sum_var/vi)

    return w_ij
def calc_weight_ijk(var):
    w=[]
    for i in range(0,len(var[0])-2):
        temp=[]
        for j in range(0,len(var)):
            #print(len(var[0]),len(var[j]))
            temp.append(var[j][i])
        w.append(calc_weight_ij(temp))
        del temp
    return w

"""
#for testing
import random
var=[]
for i in range (0,3):
    var.append([])
    for j in range(0,10):
        var[i].append(random.random())
w_ijk=calc_weight_ijk(var)
print(w_ijk)
print(np.transpose(w_ijk))
"""