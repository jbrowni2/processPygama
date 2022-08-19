import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from math import exp
import processes.foundation as fd
from math import exp, sqrt, pi, erfc
from lmfit import Model
import csv

def main():

    with open('noiseFit', newline='') as csvfile:
        noise = csv.reader(csvfile)
        ri = next(noise)
        fl = next(noise)
        f = next(noise)
        err = next(noise)
        rise = [float(x) for x in ri]
        flat = [float(x) for x in fl]
        fw = [float(x) for x in f]
        error = [float(x) for x in err]


    i = fw.index(min(fw))
    riMin = rise[i]
    flatMin = flat[i]

    indexRiMin = [i for i,x in enumerate(rise) if x==riMin]
    fwRiMin = [fw[i] for i in indexRiMin]
    flatRiMin = [flat[i] for i in indexRiMin]
    errorRiMin = [error[i] for i in indexRiMin]
    indexFlMin = [j for j,x in enumerate(flat) if x==flatMin]
    fwFlatMin = [fw[i] for i in indexFlMin]
    riseFlMin = [rise[i] for i in indexFlMin]
    errorFlMin = [error[i] for i in indexFlMin]


    plt.subplot(1,2,1)
    plt.errorbar(flatRiMin,fwRiMin,yerr=errorRiMin, fmt='o')
    plt.title("FWHM vs flat time for pulser peak with rise time 10.0 us")
    plt.xlabel("shaping (microseconds)")
    plt.ylabel("FWHM (KeV)")
    plt.rcParams['figure.facecolor'] = 'white'
    plt.subplot(1,2,2)
    plt.errorbar(riseFlMin,fwFlatMin,yerr=errorFlMin, fmt='o')
    plt.title("FWHM vs flat time for pulser peak with rise time 10.0 us")
    plt.xlabel("shaping (microseconds)")
    plt.ylabel("FWHM (KeV)")
    plt.rcParams['figure.facecolor'] = 'white'
    plt.show()




if __name__ == "__main__":
    main()
