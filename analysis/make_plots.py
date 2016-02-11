import numpy as np
from bokeh.plotting import figure, show, output_file, vplot, gridplot
from bokeh.charts import Histogram, Dot, show, output_file
from bokeh.palettes import brewer
from bokeh.models import PrintfTickFormatter
from six_bin_average import six_bin_av
from noise_dist import single_bin_dev
from noise_dist import summed_bin_dev
def make_frequency_list(f):
#create the full frequency list for plotting
    f_f=np.append(f[0],f[1])
    for i in range(2,len(f)):
        f_f=np.append(f_f,f[i])
    f_f=np.unique(f_f)

    start_f=f[len(f)-1][0]
    stop_f=f[0][len(f[0])-1]
    start_index=np.where(f_f==start_f)[0][0]+1
    stop_index=np.where(f_f==stop_f)[0][0]
    return [f_f,start_f,stop_f,start_index,stop_index]
def plot_everything(n_ss,f,f0,snr_c,sp,p,w_ij,p_pad):
    colors = ["#4F81BD","#C05061","#9BBB59","#7D60A0","#F79646","#00008B","#EE1540","#556B2F","#DDA0DD","#FF8C00"]
    output_file("grand_spec.html")
    #plot just grand spectrum
    temp=make_frequency_list(f)
    f_f,st_f,sp_f,st_i,sp_i=temp[0],temp[1],temp[2],temp[3],temp[4]
    del temp
    p1_0=figure(x_axis_label="frequency [GHz]",y_axis_label="Combined SNR")
    p1_0.line(f_f[st_i:sp_i],snr_c[st_i:sp_i])
    #plot just 6 bin averaged grand spectrum
    snr_c6=six_bin_av(snr_c[st_i:sp_i])
    f_6=six_bin_av(f_f[st_i:sp_i])
    p1_1=figure(x_axis_label="frequency [GHz]",y_axis_label="Processed Power",x_range=p1_0.x_range)
    p1_1.line(f_6,snr_c6)
    #plot all spectra
    p1=figure(x_axis_label="frequency [GHz]",y_axis_label="SNR",x_range=p1_0.x_range)
    for i in range (0,n_ss):
        p1.line(f_f,sp[i],color=colors[i%len(colors)])
    #plot the single bin deviations for each subspectra
    p2=figure(x_axis_label="Single Spectra Deviation from Mean [standard deviations]",y_axis_label="Number of bins",x_range=[-10,10],y_axis_type="log")
    #need this piece so log scale displays
    hist_pts=single_bin_dev(p)
    hist1, edges1 = np.histogram(hist_pts,bins=225)
    #need this piece so log scale displays
    for i in range(0,len(hist1)):
        if hist1[i]==0:
            hist1[i]+=1
    p2.quad(top=hist1, bottom=1, left=edges1[:-1], right=edges1[1:],color='green')
    #plot the single bin devaitions for the grand stspectra on linear and log
    hist_pts_sum=summed_bin_dev(snr_c[st_i:sp_i])
    hist2, edges2 = np.histogram(hist_pts_sum,bins=50)
    p3=figure(x_axis_label="Deviation from Grand Mean [standard deviations]",y_axis_label="dN/dσ",x_range=[-9,9])
    p3.quad(top=hist2, bottom=0, left=edges2[:-1], right=edges2[1:],color='red',legend="Data")
    hist3=list(hist2)
    edges3=list(edges2)
    #need to offset to display on log scale
    for i in range(0,len(hist3)):
        if hist3[i]==0:
            hist3[i]+=1
            edges3[i]+=1
    p3_0=figure(x_axis_label="Deviation from Grand Mean [standard deviations]",y_axis_label="dN/dσ",y_axis_type="log")
    p3_0.quad(top=hist3, bottom=1, left=edges3[:-1], right=edges3[1:],color='red',legend="Data")
    #plot the six bin devaitions for the grand stspectra both on log scale
    p3_1=figure(x_axis_label="Deviation from 6 Bin Grand Mean [standard deviations]",y_axis_label="Number of bins",y_axis_type="log")
    hist_pts_sum_6=summed_bin_dev(snr_c6)
    hist4, edges4 = np.histogram(hist_pts_sum_6,bins=20)
    hist4_log=list(hist4)
    edges4_log=list(edges4)
    for i in range(0,len(hist4_log)):
        if hist4_log[i]==0:
            hist4_log[i]+=1
            edges4_log[i]+=1
    p3_1.quad(top=hist4_log, bottom=1, left=edges4_log[:-1], right=edges4_log[1:],color='red',legend="Data")
    #plot to show the frequency space covered
    x=np.linspace(0,len(f0),len(f0))
    dw=[]
    for i in range (0,len(f)):
        dw.append((f[i][len(f[i])-1]-f[i][0])/2)
    spec_width=[]
    x_width=[]
    for i in range (0,len(f)):
        spec_width.append((f0[i]-dw[i],f0[i]+dw[i]))
        x_width.append((x[i],x[i]))
    p4=figure(x_axis_label="Tuning Steps",y_axis_label="Central Frequncy [GHz]")
    p4.diamond(x,f0)
    p4.multi_line(x_width, spec_width)
    #some formating to ensure axis line up
    p1.yaxis[0].formatter = PrintfTickFormatter(format="%5f")
    p1_0.yaxis[0].formatter = PrintfTickFormatter(format="%5f")
    p1_1.yaxis[0].formatter = PrintfTickFormatter(format="%5f")
    #plot the weighting functions
    p5=figure(x_axis_label="f")
    for i in range (0,n_ss):
        p5.line(f_f,w_ij[i],color=colors[i%len(colors)])
    #plot the padded power
    p6=figure(x_axis_label="f")
    for i in range (0,n_ss):
        p6.line(f_f,p_pad[i],color=colors[i%len(colors)])
    show (vplot(p1,p1_0,p1_1,p2,p3,p3_0,p3_1,p4,p5,p6))
    return 0
