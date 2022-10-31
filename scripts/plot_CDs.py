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
    t1_data = fd.get_t1_data(1399)

    cDs = np.array([[np.zeros(len(t1_data[0]["waveform"]["values"].nda[0]))]*4]*len(t1_data[0]["waveform"]["values"].nda))
    for i in range(0,len(t1_data[0]["waveform"]["values"].nda)):
        cDsHold = pywt.swt(t1_data[0]["waveform"]["values"].nda[i], "haar", level=4)
        for j, cd in enumerate(cDsHold):
            cDs[i][j] = cd[1]


    df = pd.DataFrame(cDs[0]).T
    print(df)



    figure, axis = plt.subplots(4, 1)
  
    # For Sine Function
    axis[0].plot(cDs[0][0])
    axis[0].set_title("The Four Levels of Wavelet Constants")
  
    # For Cosine Function
    axis[1].plot(cDs[0][1])
  
    # For Tangent Function
    axis[2].plot(cDs[0][2])
  
    # For Tanh Function
    axis[3].plot(cDs[0][3])
  
    # Combine all the operations and display
    plt.show()



    

    
    #sto.write_object(tb_wfs, f'{tb_in}', f_wfs,wo_mode='a')


if __name__ == "__main__":
    main()