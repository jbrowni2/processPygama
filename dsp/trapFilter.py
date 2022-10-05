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


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA

import scipy.signal as sig

def main():


    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    runs = [x for x in range(1364,1395)]

    f_wfs = 'opt/Run50.lh5'

    sto = LH5Store(data["tier1_dir"])

    rise = int(8*1000/8)
    flat = int(0.5*1000/8)

    trapFilter = np.zeros(2*rise + flat)

    trapFilter[0:rise] = 1.0
    trapFilter[rise+1:flat+rise] = 0.0
    trapFilter[rise+flat+1:] = -1.0






    for i,run in enumerate(runs):
        print(run)
        t1_data = fd.get_t1_data(run, "Card1")
        print(t1_data[0])


        trapWave = np.zeros((len(t1_data[0]["waveform"]["values"].nda), len(t1_data[0]["waveform"]["values"].nda[0])- len(trapFilter)+1))
        for i,wave in enumerate(t1_data[0]["waveform"]["values"].nda):
            trapWave[i] = sig.convolve(wave, trapFilter, "valid")

        

        runstr = "Run"+str(run)+".lh5"

        tb_in = 'Card1'

        sto.write_object(trapWave, f'{tb_in}', f_wfs,wo_mode='a')

if __name__ == "__main__":
    main()