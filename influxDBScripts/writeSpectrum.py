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
    data = fd.get_df(run_list, "Card1")
    m = 0.0408625 #kev/adc
    b = -0.16892
    data["energy"] = m*data["trapEmax"] + b
    
    for i,energy in enumerate(data["energy"]):
        client = InfluxDBClient(url="http://localhost:8086", username="jlb1694", password="Jlb2360$", org="gemini")

        query_api = client.query_api()
        write_api = client.write_api(write_options=SYNCHRONOUS)

        _point1 = Point("Detector_energy").tag("channel", data["channel"].iloc[i]).field("energy", energy)

        write_api.write(bucket="detectorSpec2", record=_point1)

    data_frame = query_api.query_data_frame('from(bucket:"detectorSpec2") '
                                        '|> range(start: -10m) '
                                        '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") '
                                        '|> keep(columns: ["channel", "energy"])')
    print(data_frame.to_string())

    client.close() 
    

if __name__ == "__main__":
    main()