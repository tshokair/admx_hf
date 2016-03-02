"""
    read_header.py Author T. Shokair 9/11/15
    function to read in the header file and return the values needed for data processing.
    
    """
def read_head(f):
    searchfile = open(f, "r")
    for line in searchfile:
        if "Cavity freq (GHz)" in line:
            cf_l=line.split()
            cf=float(cf_l[3])
        elif "Cavity Q" in line:
            q_l=line.split()
            q=float(q_l[2])
        elif "Freq change/cavity step (GHz)" in line:
            fs_l=line.split()
            print(fs_l)
            fs=float(fs_l[4])
        elif "FFT size (pts)" in line:
            pt_l=line.split()
            pt=int(pt_l[3])
        elif "GaGe sample rate:" in line:
            sr_l=line.split()
            sr=int(sr_l[3])
        elif "Freq center (GHz):" in line:
            fc_l=line.split()
            fc=float(fc_l[3])
        elif "Freq width (GHz):" in line:
            fw_l=line.split()
            fw=float(fw_l[3])
    #print(sr)
    searchfile.close()
    st=sr*1E-3/pt
    #print("step size",st,sr,pt)
    return [cf,q,st,fc,fw,pt]
