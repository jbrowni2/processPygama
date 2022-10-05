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


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA


def main():
    #Here we set the range of the files
    hi = 50
    lo = 30


    #Here you set the calibration
    m = 0.04280811709355686
    c = -0.04784377473936274

    #find the files
    runs = [x for x in range(1396,1407)]
    #run = 1289
    #name the output file
    f_wfs = 'opt/Run2.lh5'


    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    sto = LH5Store(data["tier1_dir"])
    """
    t2_data = fd.get_df(run, 'Card1')

    t2_data["trapEmax"] = m*t2_data["trapEmax"] + c
    
    ecuthi = t2_data["trapEmax"] < hi 
    ecutlo = t2_data["trapEmax"] > lo

    filter_idx = np.asarray(t2_data.index[ecuthi&ecutlo].tolist())
        #slim_filter = np.random.choice(filter_idx, nevts)
        #slim_filter = np.unique(slim_filter)

    runstr = "Run"+str(run)+".lh5"

    tb_in = 'Card1'

    tb_wfs, nwfs = sto.read_object('Card1/',[runstr],idx=filter_idx)
    sto.write_object(tb_wfs, f'{tb_in}', f_wfs,wo_mode='a')

    nevts = 150

    """
    for i,run in enumerate(runs):

        t2_data = fd.get_df(run, 'Card1')

        t2_data["trapEmax"] = m*t2_data["trapEmax"] + c
    
        ecuthi = t2_data["trapEmax"] < hi 
        ecutlo = t2_data["trapEmax"] > lo

        filter_idx = np.asarray(t2_data.index[ecuthi&ecutlo].tolist())
        #slim_filter = np.random.choice(filter_idx, nevts)
        #slim_filter = np.unique(slim_filter)

        runstr = "Run"+str(run)+".lh5"

        tb_in = 'Card1'

        tb_wfs, nwfs = sto.read_object('Card1/',[runstr],idx=filter_idx)
        sto.write_object(tb_wfs, f'{tb_in}', f_wfs,wo_mode='a')


if __name__ == "__main__":
    main()