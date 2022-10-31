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


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def main():
    df = fd.get_t1_data(6994)
    triggerRate = len(df[0]["waveform"]["values"].nda)

    print(triggerRate)


    
    client = InfluxDBClient(url="http://localhost:8086", username="jlb1694", password="Jlb2360$", org="gemini")

    query_api = client.query_api()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    
    _point1 = Point("Muon_Veto_TriggerRate").tag("channel", "muonVeto").field("triggerRate", triggerRate)

    write_api.write(bucket="muonTrigger", record=_point1)

    client.close()

if __name__ == "__main__":
    main()