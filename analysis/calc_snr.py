import numpy as np
import math
k=1.380e-23
def ps_calc(f,cf,df,q):
    coef=6.21e-28
    beta=1.4
    B=9
    C=1.5
    V=0.0015
    A=coef*2*math.pi*B*B*V*beta/(beta+1)*C*q
    return [A*x*(1/(1+(2*(x-cf)/df)**2)) for x in f]

def var_calc(p,T,f,cf,df,q):
    mu=np.average(p)
    ps=ps_calc(f,cf,df,q)
    var=[(a-mu)**2 for a in p]
    var_av=(1/len(p))*np.sum(var)
    sig=math.sqrt(var_av)
    sig_s=[k*T*df*sig/b for b in ps]
    return [a**2 for a in sig_s]

def delta_calc(p,T,f,cf,df,q):
    ps=ps_calc(f,cf,df,q)
    del_ij=[k*T*df*a/b for a,b in zip(p,ps)]
    return del_ij

