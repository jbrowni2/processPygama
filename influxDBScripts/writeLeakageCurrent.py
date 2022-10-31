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


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def line(x, A, B): # this is your 'straight line' y=f(x)
    return A*x + B

def main():
    run_list = 1363
    data = fd.get_t1_data(run_list, "Card1")

    for i in range(0,8):
        wave = data[0]["waveform"]["values"].nda[i]
        timestamp = data[0]["timestamp"].nda[i]*8
        channel = data[0]["channel"].nda[i]

        xdata = np.arange(0,15000,1)
        popt, pcov = curve_fit(line, xdata, wave[0:15000])

        x = popt[0] #adc/clock ticks
        m = 0.0408625 #kev/adc
        b = -0.16892 #kev
        amp = 6.241509 * pow(10,18)
        eV_per_ns = (1000. * m)*x + (1000./8)*pow(10,-9)*b
        e_per_ns = eV_per_ns / 2.9
        e_per_s = e_per_ns * pow(10,9)
        pA = (e_per_s / amp) * pow(10,12)

        if pA <= 0.001:
            continue

    
        client = InfluxDBClient(url="http://localhost:8086", username="jlb1694", password="Jlb2360$", org="gemini")

        query_api = client.query_api()
        write_api = client.write_api(write_options=SYNCHRONOUS)

        _point1 = Point("Detector_Leakage_Current").tag("channel", i).field("Leakage Current", pA).field("timestamp", timestamp)

        write_api.write(bucket="leakageTest", record=_point1)


    client.close() 
    

if __name__ == "__main__":
    main()