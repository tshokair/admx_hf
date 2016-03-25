import pickle
from bokeh.plotting import figure, show, output_file, vplot, gridplot
f_f=pickle.load(open('full_f.pkl','rb'))
offset_normed_sig=pickle.load(open('offset_normed_sig.pkl','rb'))
normed_signal_c=pickle.load(open('normed_signal_c.pkl','rb'))
output_file('sub_and_grand.html')
p1=figure(x_axis_label="frequency [GHz]",y_axis_label="Normalized Signal")
colors = ["#4F81BD","#C05061","#9BBB59","#7D60A0","#F79646","#00008B","#EE1540","#556B2F","#DDA0DD","#FF8C00"]
n_ss=len(offset_normed_sig)
for i in range (0,n_ss):
    p1.line(f_f,offset_normed_sig[i],color=colors[i%len(colors)])
#show(p1)
p_0=[]
p=[]
n_plots=len(f_f)//1350
print(n_plots)
for j in range(0,n_plots):
    p_0.append(figure(x_axis_label="frequency [GHz]",y_axis_label="Combined Normalized Signal"))
    p.append(figure(x_axis_label="frequency [GHz]",y_axis_label="Normalized Signal",x_range=p_0[j].x_range))
    for i in range (0,n_ss):
        p[j].line(f_f[j*1350:(j+1)*1350],offset_normed_sig[i][j*1350:(j+1)*1350],color=colors[i%len(colors)])
        p_0[j].line(f_f[j*1350:(j+1)*1350],normed_signal_c[j*1350:(j+1)*1350])
show(gridplot([[p[0],p[1],p[2],p[3]],[p_0[0],p_0[1],p_0[2],p_0[3]]]))
