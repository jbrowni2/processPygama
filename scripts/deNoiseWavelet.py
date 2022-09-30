"""
This filter was written by Ryan B.
This filter takes in a processed pygama file and reduces it into a desired energy range.
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
import pywt
from statistics import median


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA


def main():

    #find the files
    runs = [x for x in range(9189,9209)]
    f_wfs = ["run" + str(i) + ".lh5" for i in range(2,len(runs)+1)]


    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    sto = LH5Store(data["tier1_dir"])

    n=0
    for run in runs:
        print(n)

        data1 = fd.get_t1_data(run, "Card1")
        for i in range(0,len(data1[0]["waveform"]["values"].nda)):
        #for i in range(0,30):
            cDs = pywt.swt(data1[0]["waveform"]["values"].nda[i], "haar", level=4)
            threshold = np.zeros_like([0,0,0,0])

            j = 0
            for cD in cDs:
                median_value = median(cD[1])
                median_average_deviation = median([abs(number-median_value) for number in cD[1]])
                sig1 = median_average_deviation/0.6745
                threshold[j] = sig1*np.sqrt(2*np.log(len(data1[0]["waveform"]["values"].nda[i])))
                j+=1

            j = 0
            for cD in cDs:
                cD[1][abs(cD[1]) < threshold[j]] = 0.0
                j += 1

            data1[0]["waveform"]["values"].nda[i] = pywt.iswt(cDs, "Haar")

        tb_in = 'Card1'
    
        sto.write_object(data1[0], f'{tb_in}', f_wfs[n],wo_mode='a')
        n+=1

    

    
    #sto.write_object(tb_wfs, f'{tb_in}', f_wfs,wo_mode='a')


if __name__ == "__main__":
    main()