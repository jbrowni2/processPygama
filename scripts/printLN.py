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

def getLN(run):
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    t1_dir = data['tier1_dir']


    f_raw = t1_dir + '/Run' + str(run) + '.lh5'
    raw_store = lh5.LH5Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = lh5.ls(f_raw)
    print(lh5_keys)
    buffer_len = 10000000000000000
    t1_data = []


    tot_n_rows = raw_store.read_n_rows(lh5_keys[1], f_raw)

    chan_name = lh5_keys[1].split('/')[0]
    LN, n_rows_read = raw_store.read_object(lh5_keys[1], f_raw, start_row=0, n_rows=buffer_len)

    dictionary = dict()
    for col in LN:
        dictionary[col] = LN[col].nda

    df = pd.DataFrame(data=dictionary)
    return df


def main():
    df = getLN(7024)
    print(df)

if __name__ == "__main__":
    main()