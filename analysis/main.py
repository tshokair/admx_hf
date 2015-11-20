"""
    main.py Author T. Shokair 9/11/15
    This main function reads in a list of power spectra, calls a function to process them, coadds each processed spectra, and finally plots a grand spectrum.
    updated 10/8/15 to fix some bugs with coadding and incorporate histogram plotting
    
"""
import numpy as np
import random
from scipy import signal
from scipy import optimize
from scipy.stats import norm
import pylab as pl
import matplotlib.pyplot as plt
import time
from process_spectra import process
from pad_list import find_pad_param
from pad_list import pad_l
from noise_dist import single_bin_dev
from noise_dist import summed_bin_dev
from sort_spec import sort_from_indexes
import pickle
from bokeh.plotting import figure, show, output_file, vplot, gridplot
from bokeh.charts import Histogram, Dot, show, output_file
from bokeh.palettes import brewer
from fit_gauss import fit
from count_contributing_bins import count_f_per_bin
from six_bin_average import six_bin_av
#a file named p_spectra.txt should contain all of the runs to be included in a grand spectrum
runF=open("p_spectra.txt","r")
r_in=runF.readlines()
rn=list(map(int,r_in))
f0=[]
# lists to fill
p_uns=[]
f_uns=[]
f0_uns=[]
fs_uns=[]
wf=[]
wp=[]
#n_ss=len(rn)
n_ss=7
#Call functions to process data and fill lists
for i in range (0,n_ss):
    print("Processing",rn[i])
    ls=process(rn[i])
    p_uns.append(ls[5])
    f0_uns.append(ls[2])
    f_uns.append(ls[0])
    fs_uns.append(ls[3])
    #print(len(ls[1]))
    del ls
f_start=[item[0] for item in f_uns ]
s_ind=np.argsort(f_start)
f=sort_from_indexes(s_ind,f_uns)
p=sort_from_indexes(s_ind,p_uns)
f0=sort_from_indexes(s_ind,f0_uns)
fs=sort_from_indexes(s_ind,fs_uns)

#pad each list so they can be added together
x=np.linspace(0,len(f0),len(f0))
dw=[]
for i in range (0,len(f)):
    dw.append((f[i][len(f[i])-1]-f[i][0])/2)
pad_param=find_pad_param(f,fs[0])
print(pad_param)
wp=[]
for i in range(0,n_ss):
    wp.append(pad_l(f[i],pad_param,p[i]))

wp_t=[a for a in wp[0]]
#sum the powers and offset the subspectra for plotting
#sp are offset spectra, offset simply for plotting purposes.

sp=[]
sp.append([a+.1 for a in p[0]])
for i in range (1,n_ss):
    sp.append([a+.1*(i%19+1) for a in p[i]])
    wp_t=[a+b for a,b in zip(wp_t,wp[i])]
#create the full frequency list
f_t=np.linspace(pad_param[0],pad_param[1],pad_param[2])
#weight the powers by the number of contibuting bins
f_per_bin=count_f_per_bin(f,f_t[0],f_t[len(f_t)-1],fs[0])
for i in range (0,len(wp_t)):
    if f_per_bin[i]>0:
        wp_t[i]=wp_t[i]/f_per_bin[i]
#comment below if using bokeh instead of matplotlib
"""
#plot grand spectrum
pl.subplot(311)
pl.plot(f_t[0:len(wp_t)],wp_t)
#plot the individual subspectra
for i in range (0,n_ss):
    #print(len(f[i]),len(sp[i]))
    pl.plot(f[i][0:len(sp[i])],sp[i])
pl.ylabel('Power ')
pl.xlabel('Frequncy [GHz]')
#pl.show()

#
# plot the noise distributions
pl.subplot(312)
hist_pts=single_bin_dev(p)
hist_pts_sum=summed_bin_dev(p)
n1, bins1, patches1 = pl.hist(hist_pts, 500, normed=1, histtype='stepfilled')
pl.title("Single Spectra")
pl.yscale('log')
pl.ylabel('entries')
pl.xlabel('sigma')
pl.subplot(313)
n2 = pl.hist(hist_pts_sum, 500, normed=1, histtype='stepfilled')
pl.title("Summed Spectra")
pl.yscale('log')
pl.ylabel('entries')
pl.xlabel('sigma')
pl.show()
"""
#uncomment below if Bokeh is installed on the machine running the code. Comment the above out to remove Matplotlib plots

colors = ["#4F81BD","#C05061","#9BBB59","#7D60A0","#F79646","#00008B","#EE1540","#556B2F","#DDA0DD","#FF8C00"]
output_file("grand_spec.html")
#plot just grand spectrum
p1_0=figure(x_axis_label="frequency [GHz]",y_axis_label="Processed Power")
p1_0.line(f_t[0:len(wp_t)],wp_t)
#plot just 6 bin averaged grand spectrum
wp_t6=six_bin_av(wp_t)
f_t6=six_bin_av(f_t)
p1_1=figure(x_axis_label="frequency [GHz]",y_axis_label="Processed Power",x_range=p1_0.x_range)
p1_1.line(f_t6,wp_t6)
#plot all spectra
p1=figure(x_axis_label="frequency [GHz]",y_axis_label="Processed Power",x_range=p1_0.x_range)
#p1.line(f_t[0:len(wp_t)],wp_t)
for i in range (0,n_ss):
    p1.line(f[i],sp[i],color=colors[i%len(colors)])



#plot the single bin deviations for each subspectra
p2=figure(x_axis_label="Single Spectra Deviation from Mean [standard deviations]",y_axis_label="Number of bins",x_range=[-10,10],y_axis_type="log")
hist_pts=single_bin_dev(p)
hist1, edges1 = np.histogram(hist_pts,bins=225)
#need this piece so log scale displays
for i in range(0,len(hist1)):
    if hist1[i]==0:
        hist1[i]+=1
p2.quad(top=hist1, bottom=1, left=edges1[:-1], right=edges1[1:],color='green')
#plot the single bin devaitions for the grand spectra both on linear and log scales
p3=figure(x_axis_label="Deviation from Grand Mean [standard deviations]",y_axis_label="Number of bins",x_range=[-9,9])
#,y_axis_type="log", y_range=[0, 17000]
hist_pts_sum=summed_bin_dev(wp_t)
hist2, edges2 = np.histogram(hist_pts_sum,bins=1000)
p3.quad(top=hist2, bottom=0, left=edges2[:-1], right=edges2[1:],color='red',legend="Data")
p3_0=figure(x_axis_label="Deviation from Grand Mean [standard deviations]",y_axis_label="Number of bins",y_axis_type="log")
hist3=list(hist2)
edges3=list(edges2)

for i in range(0,len(hist3)):
    if hist3[i]==0:
        hist3[i]+=1
        edges3[i]+=1
p3_0.quad(top=hist3, bottom=1, left=edges3[:-1], right=edges3[1:],color='red',legend="Data")
bin_centres = (edges2[:-1] + edges2[1:])/2
gauss_fit=fit(bin_centres,hist2)
p3.line(edges2,gauss_fit, color="black",line_width=3,legend="Gaussian Fit")
#plot the deviations from a six bin average
hist_pts_sum_6=summed_bin_dev(six_bin_av(wp_t))
hist4, edges4 = np.histogram(hist_pts_sum_6,bins=1000)

p3_1=figure(x_axis_label="Deviation from 6 Bin Grand Mean [standard deviations]",y_axis_label="Number of bins",y_axis_type="log")
hist4_1=list(hist4)
edges4_1=list(edges4)

for i in range(0,len(hist4_1)):
    if hist4_1[i]==0:
        hist4_1[i]+=1
        edges4_1[i]+=1
p3_1.quad(top=hist4_1, bottom=1, left=edges4_1[:-1], right=edges4_1[1:],color='red',legend="Data")




spec_width=[]
x_width=[]
for i in range (0,len(f)):
    spec_width.append((f0[i]-dw[i],f0[i]+dw[i]))
    x_width.append((x[i],x[i]))
p4=figure(x_axis_label="Tuning Steps",y_axis_label="Central Frequncy [GHz]")
p4.diamond(x,f0)
p4.multi_line(x_width, spec_width)
show (vplot(p1,p1_0,p1_1,p2,p3,p3_0,p3_1,p4))



