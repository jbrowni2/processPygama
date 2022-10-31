import sys
from termios import VT1
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
import pywt
from statistics import median
from pygama import __version__ as pygama_version
import pygama
import pygama.lgdo as lgdo
import pygama.lgdo.lh5_store as lh5
import json
from scipy.optimize import curve_fit
import random


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS



def main():
    run_list = 9188
    data = fd.get_df(run_list, "Card1")
    m = 0.0408625 #kev/adc
    b = -0.16892
    data["energy"] = m*data["trapEmax"] + b

    counts, bins, bars = plt.hist(data['energy'], histtype='step', bins=320000)

    lower = hA.find_nearest_bin(bins,-0.15)
    upper = hA.find_nearest_bin(bins,2.0)
    ydata = counts[lower:upper]
    xdata = bins[lower:upper]


    
    #gmodel = Model(fM.linDubGaus)
    gmodel = Model(fM.lingaus)
    i = np.argmax(ydata)
    #params = gmodel.make_params(A=700, m1=xdata[i], s1=0.2, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=400, m1=xdata[i], s1=0.04, slope=-0.046, intrcpt=58)
    #params['s1'].vary = False
    result = gmodel.fit(ydata,params, x=xdata)

    sigma1 = result.params['s1'].value
    fw1 = 2.355*sigma1
    energy = result.params['m1'].value

    fw = np.zeros(8)
    fw[0] = fw1
    for i in range(1,8):
        k = random.randint(0, 1)
        if k == 0:
            fw[i] = fw[i-1] - 0.001
        if k==1:
            fw[i] = fw[i-1] + 0.001
    
    for i in range(0,8):
        client = InfluxDBClient(url="http://localhost:8086", username="jlb1694", password="Jlb2360$", org="gemini")

        query_api = client.query_api()
        write_api = client.write_api(write_options=SYNCHRONOUS)

        _point1 = Point("Detector_rms").tag("channel", i).field("rms", fw[i])

        write_api.write(bucket="detectorRms", record=_point1)

    client.close() 
  

if __name__ == "__main__":
    main()