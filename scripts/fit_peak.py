import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from math import exp
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
from math import exp, sqrt, pi, erfc
from lmfit import Model


def main():
   # run_list = [x for x in range(1364,1366)]
    #t2_data1 = fd.get_df_multiple(run_list, "Card1")
    #run_list = [x for x in range(1367,1388)]
    #t2_data2 = fd.get_df_multiple(run_list, "Card1")
    #run_list = [x for x in range(1390,1396)]
    #t2_data3 = fd.get_df_multiple(run_list, "Card1")
    #t2_data = pd.concat([t2_data1, t2_data2, t2_data3])
    #c = 0.0428
    #m = -0.193

    run_list = [x for x in range(1330,1361)]
    t2_data = fd.get_df_multiple(run_list, "Card1")
    c =0.0408625
    m = -0.16892
    t2_data["calEnergy"] = t2_data["trapEmax"]*c + m 

    counts, bins, bars = plt.hist(t2_data['calEnergy'], histtype='step', bins=1200000)

    lower = hA.find_nearest_bin(bins,-0.15)
    upper = hA.find_nearest_bin(bins, 0.3)
    ydata = counts[lower:upper]
    xdata = bins[lower:upper]


    """
    gmodel = Model(fM.linDubGaus)
    i = np.argmax(ydata)
    #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=400, m1=xdata[i], s1=0.07, a2=400, m2=xdata[i]+0.15, s2=0.07, slope=-0.046, intrcpt=58)
    #params['s1'].vary = False
    result = gmodel.fit(ydata,params, x=xdata)

    sigma1 = result.params['s1'].value
    fw1 = 2.355*sigma1
    sigma2 = result.params['s2'].value
    fw2 = 2.355*sigma2
    energy = result.params['m1'].value
    print(fw1)
    print(fw2)
    """
    gmodel = Model(fM.lingaus)
    i = np.argmax(ydata)
    #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=300, m1=xdata[i], s1=0.05, slope=-0.046, intrcpt=58)
    #params['s1'].vary = False
    result = gmodel.fit(ydata,params, x=xdata)

    sigma = result.params['s1'].value
    fw = 2.355*sigma
    err = 2.355*result.params['s1'].stderr
    energy = result.params['m1'].value
    print(fw)
    print(err)

    

    #plt.hist(t2_data['calEnergy'], histtype='step', bins=900000)
    plt.xlim(-0.15, 0.25)
    plt.ylim(0, 30000)
    plt.xlabel("Energy [keV]")
    plt.ylabel("Counts")
    plt.plot(xdata, result.best_fit, 'r-', label='best fit')
    plt.text(-0.12,28000, "FWHM = 0.0776(5) keV")
    plt.title("Fit of RMS Noise from Ge Detector 1724")
    plt.show()




if __name__ == "__main__":
    main()
