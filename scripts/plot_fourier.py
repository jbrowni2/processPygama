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
    wave = t1_data[0]["waveform"]["values"].nda[0]

    fourier = np.abs(np.fft.fft(wave[0:10000]))**2
    freqs = abs(np.fft.fftfreq(len(wave[0:10000])))
    idx = np.argsort(freqs)

    plt.plot(freqs[1:], fourier[1:])

  
    # Combine all the operations and display
    plt.show()



    

    
    #sto.write_object(tb_wfs, f'{tb_in}', f_wfs,wo_mode='a')


if __name__ == "__main__":
    main()