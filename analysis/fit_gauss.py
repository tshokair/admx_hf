import numpy as np
from scipy.optimize import curve_fit
# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

def fit(x,hist):
    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    p0 = [1., 0., 1.]

    coeff, var_matrix = curve_fit(gauss, x, hist, p0=p0)

    # Get the fitted curve
    hist_fit = gauss(x, *coeff)
    return hist_fit




