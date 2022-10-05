"""
This filter was written by James B.
This script was written to fit noise data.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py 
import json
import copy
from collections import OrderedDict
from lmfit import Model
import os

from pygama.pargen.dsp_optimize import run_one_dsp
from pygama.pargen.dsp_optimize import run_grid
from pygama.pargen.dsp_optimize import ParGrid
from pygama.lgdo.lh5_store import LH5Store
import pygama.math.histogram as pgh
import pygama.math.peak_fitting as pgf



import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA


def main():
    df = pd.read_csv('RiseNoiseChange1725Sub2.csv')

    df["FW2"] = df["FWHM"]**2
    #df["rise"] = np.linspace(3,20,18)
    df["err2"] = df["FW2"]*(df["error"]/df["FWHM"])
    print(df)
    print(min(df["FWHM"].iloc))

    gmodel = Model(fM.noise)
    params = gmodel.make_params(h1=0.0006, h2=0.06, h3=0.0001)
    params["h3"].min = 0.0
    result = gmodel.fit(df["FW2"].values[0:45],params, x=df["rise"].values[0:45])

    print(result.fit_report())

    h1 = result.params['h1'].value
    h2 = result.params["h2"].value
    h3 = result.params["h3"].value

    x = np.linspace(1.0,15.0,1000)
    y = fM.noise(x, h1, h2, h3)
    y1 = h1*x
    y2 = h2/x
    y3 = np.ones(len(x))*h3
    print(h3)

    plt.errorbar(df["rise"].values[0:45], df["FW2"].values[0:45], yerr=df["err2"].values[0:45], fmt='bo')
    plt.plot(x,y, '-r', label="Fit")
    plt.plot(x, y1, 'g--', label="Parrallel")
    plt.plot(x, y2, 'b--', label="Series")
    plt.plot(x, y3, 'y', label="White Noise")
    plt.legend()
    plt.xlabel("Rise [us]")
    plt.ylabel("FWHM^2 [keV^2]")
    plt.title("FWHM^2 of Pulsar Peak as a Function of Rise Time For 1725 Subtract Second")
    plt.text(8, 0.065,"Fit = h1*x + h2/x + h3")
    plt.text(8, 0.06, "h1 = 0.00058(3)")
    plt.text(8, 0.055, "h2 = 0.0570(8)")
    plt.text(8, 0.05, "h3 = 0.0099(5)")
    plt.show()



if __name__ == "__main__":
    main()