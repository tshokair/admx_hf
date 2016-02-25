def make_par_array(date):
    f=open('/mnt/nfs/admx/admx-hf_data/experimentData/'+date+'/'+date+'_0_00000.par','r')
    cl_in=f.readline()
    cl_name=str.split(cl_in)
    pars=[]
    for line in f:
        st_in=str.split(line)
        pars.append(st_in)
    return pars

def read_header(date):
    f=open('/mnt/nfs/admx/admx-hf_data/experimentData/'+date+'/'+date+'_0_00000.hdr','r')
    for line in f:
        if "Sample rate:" in line:
            sr_l=line.split()
            sr=int(sr_l[2])
        elif "FFT size (pts)" in line:
            pt_l=line.split()
            pt=int(pt_l[3])
    #Return the frequency bin size in GHz
    return sr*1E-3/pt

