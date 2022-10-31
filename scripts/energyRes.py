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
import json


def main():

    
    run_list = [x for x in range(1364,1366)]
    t2_data1 = fd.get_df_multiple(run_list, "Card1")
    run_list = [x for x in range(1367,1388)]
    t2_data2 = fd.get_df_multiple(run_list, "Card1")
    run_list = [x for x in range(1390,1396)]
    t2_data3 = fd.get_df_multiple(run_list, "Card1")
    t2_data = pd.concat([t2_data1, t2_data2, t2_data3])
    c = 0.0428
    m = -0.193
    t2_data["calEnergy"] = t2_data["trapEmax"]*c + m
    

    #run_list = [x for x in range(1330,1361)]
    #t2_data = fd.get_df_multiple(run_list, "Card1")
    c =0.0428,
    m = -0.193
    t2_data["calEnergy"] = t2_data["trapEmax"]*c + m 

    energy_list = [121, 244, 344, 411, 444,778, 866, 967, 1085, 1107, 1408]
    #energy_list = [121, 244, 344]
    fw = np.zeros_like(energy_list, dtype=np.float64)
    energ = np.zeros_like(energy_list, dtype=np.float64)
    err = np.zeros_like(energy_list, dtype=np.float64)

    counts, bins, bars = plt.hist(t2_data["calEnergy"], histtype="step", bins=60000)

    i = 0
    for energy in energy_list:
        lower = hA.find_nearest_bin(bins,energy-20)
        upper = hA.find_nearest_bin(bins,energy+20)
        ydata = counts[lower:upper]
        xdata = bins[lower:upper]
        j = np.argmax(ydata)

        gmodel = Model(fM.lingaus)
        #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
        params = gmodel.make_params(a1=300, m1=xdata[j], s1=0.3, slope=-0.046, intrcpt=58)
        #params['s1'].vary = False
        result = gmodel.fit(ydata,params, x=xdata)

        sigma = result.params['s1'].value

        fw[i] = 2.355*sigma
        err[i] = 2.355*result.params['s1'].stderr
        energ[i] = float(result.params['m1'].value)

        i+=1


    print(fw)
    print(energ)

    #This code fits the resolution map to the equation it should follow.
    gmodel = Model(fM.energyResolution)
    #params = gmodel.make_params(A=200, m1=277, s1=0.9, H_tail=-1, H_step=-1, tau=-1, slope=-0.12, intrcpt=180)
    params = gmodel.make_params(m=0.02, c=0.015, intrcpt=0.135)
    params['intrcpt'].vary = False
    params['intrcpt'].min = 0.0
    params['m'].vary = False
    params['c'].vary = False
    params['c'].min = 0.0
    result = gmodel.fit(fw,params, x=energy)



    m = result.params['m'].value
    c = result.params['c'].value
    intrcpt = result.params['intrcpt'].value
    x = np.arange(0,1500,0.1)
    y = m*np.power(x + c*(np.power(x,2)),0.5) + intrcpt

    plt.figure().clear()

    plt.errorbar(energ,fw,yerr=err, fmt='o')
    plt.plot(x,y)
    plt.title("Energy Resolution of Detector 1725 Forced Fit")
    plt.text(0,3.0, "Function is m*(E + c*(E^2)) + b")
    plt.text(0,2.0,"m = 0.02")
    plt.text(0,1.8,"c = 0.015")
    plt.text(0,1.6,"b = 0.135")
    plt.xlabel("Energy [KeV]")
    plt.ylabel("FWHM")
    #plt.ylim(0,3.2)
    plt.show()

    print('m',m)
    print('c',c)
    print('intrcpt', intrcpt)



if __name__ == "__main__":
    main()















"""
runs = [1128,1129,1130]
t2_data = fd.get_df_multiple(runs, 'Card1')


counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)
lower = fd.find_nearest_bin(bins,620)
upper = fd.find_nearest_bin(bins,700)
ydata = counts[lower:upper]
xdata = bins[lower:upper]



gmodel = Model(fd.lingaus)
#params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
params = gmodel.make_params(a1=1000, m1=660, s1=2.0, slope=-0.046, intrcpt=58)
#params['s1'].vary = False
result = gmodel.fit(ydata,params, x=xdata)

print(result.fit_report())
plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)
plt.xlim(620, 700)
plt.ylim(0,1000)
plt.xlabel("Energy [keV]")
#plt.text(76.5,1000, "FWHM = 0.459(4) keV")
plt.plot(xdata, result.best_fit, 'r-', label='best fit')
plt.title("Fit of Noise from Ge Detector")
plt.show()

sigma = result.params['s1'].value
FWHM = 2.355*sigma
err2 = 2.355*result.params['s1'].stderr



fw = [FWHM]
energy = [result.params['m1'].value]
yerr = [err2]
"""
