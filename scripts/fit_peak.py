import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from math import exp
import processes.foundation as fd
from math import exp, sqrt, pi, erfc
from lmfit import Model


def main():

    t2_data = fd.get_df(1124, 'Card1')

    counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)

    lower = fd.find_nearest_bin(bins,60)
    upper = fd.find_nearest_bin(bins,90)
    ydata = counts[lower:upper]
    xdata = bins[lower:upper]

    gmodel = Model(fd.lingaus)
    i = np.argmax(ydata)
    #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=1000, m1=xdata[i], s1=2.0, slope=-0.046, intrcpt=58)
    #params['s1'].vary = False
    result = gmodel.fit(ydata,params, x=xdata)

    sigma = result.params['s1'].value
    fw = 2.355*sigma
    energy = result.params['m1'].value

    print(fw)


    '''
    print(result.fit_report())
    plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)
    plt.xlim(75, 85)
    plt.ylim(0,2000)
    plt.xlabel("Energy [keV]")
    #plt.text(76.5,1000, "FWHM = 0.459(4) keV")
    plt.plot(xdata, result.best_fit, 'r-', label='best fit')
    plt.title("Fit of Noise from Ge Detector")
    plt.show()
    '''




if __name__ == "__main__":
    main()
