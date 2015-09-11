import numpy as np
import matplotlib.pyplot as plt
from process_spectra import process
rn=[201507310008,201507310016,201507310023,201507310030,201507310037,201507310044,201507310051,201507310059,201507310066]
f0=[]
# lists to fill
p=[]
f=[]
wf=[]
wp=[]
n_ss=len(rn)
#n_ss=7
#fill frequncy list with sequential steps
#fill power with random gaussian noise or artificial peak at 5.723968... GHz
for i in range (0,n_ss):
    ls=process(rn[i])
    f0.append(ls[2])
    del ls
x=np.linspace(0,len(f0),len(f0))
plt.plot(x,f0,'ro')
plt.show()