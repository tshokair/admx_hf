import numpy as np
from scipy.optimize import curve_fit
# Define model function to be used to fit to the data above:
def jpa_shape(x, *p):
    #A,B,C,D,E,F,G,H,I=p
    #A,B,C,E,Gam,f0=p
    A,B,E,Gam,f0=p
    #A+B*x+C*x**2+D*x**3+(1/2)*E*Gam/((x-f0)**2+(Gam/2)**2)
    return np.convolve(A*np.exp(-B*x),E*Gam/((x-f0)**2+(Gam)**2))
    #return -A/(1+np.exp(-B*(x-C)))
#return (A/(B*np.sqrt(np.pi*2)))*np.exp(-(x-C)**2/(2*B**2))+(D/(E*np.sqrt(np.pi*2)))*np.exp(-(x-F)**2/(2*E**2))+(G/np.pi)*(H/((x-I)**2+H**2))
def fit(x,pts,f0,gam):
    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    p0 = [1,1,0,gam,f0]
    #p0 = [1,1,1,gam/2,f0]
    #p0=[0.5,0.5,0.5,0.5,0.1,0.1,0.1,gam,f0]
    coeff, var_matrix = curve_fit(jpa_shape, x, pts, p0=p0)
    print(coeff)
    # Get the fitted curve
    jpa_fit = jpa_shape(x, *coeff)
    return jpa_fit




