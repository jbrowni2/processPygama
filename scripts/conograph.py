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
import multiprocessing as mp



import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA




def peak_width(tb, verbosity, make_plot=False):

    m = 0.0428
    b = -0.193
    calib = m*tb['trapEmax'].nda + b

    binning = np.linspace(30,50,num=30000)
    
    energy = copy.deepcopy(calib)
    #counts, bins, bars = plt.hist(energy, histtype='step', bins=100000)
    counts, bins = np.histogram(energy,bins=binning)

    lower = hA.find_nearest_bin(bins,30)
    upper = hA.find_nearest_bin(bins,50)
    ydata = counts[lower:upper]
    xdata = bins[lower:upper]

    gmodel = Model(fM.linDubGaus)
    i = np.argmax(ydata)
    #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=400, m1=xdata[i], s1=0.07, a2=400, m2=xdata[i]+0.2, s2=0.07, slope=-0.046, intrcpt=58)
    #params['s1'].vary = False
    result = gmodel.fit(ydata,params, x=xdata)

    sigma1 = result.params['s1'].value
    fw1 = 2.355*sigma1
    err = result.params['s1'].stderr
    err1 = err*2.355
    sigma2 = result.params['s2'].value
    fw2 = 2.355*sigma2
    err = result.params['s2'].stderr
    err2 = err*2.355
    energy = result.params['m1'].value

    print(fw1)
    print(fw2)
    #sigma = result.params['s1'].value
    #fw = 2.355*sigma
    #energy = result.params['m1'].value
    return fw1, err1

def noiseFit(i,flat, rise, dsp_config, tb_wfs):
    flat_units = str(flat)+'*us'
    rise_units = str(rise)+'*us'
    args = ['waveform',rise_units,flat_units,'wf_trap']
    dsp_config['processors']['wf_trap']['args'] = args

    fom = run_one_dsp(tb_wfs, dsp_config,fom_function=peak_width, verbosity=True)
    #fom = run_one_dsp(tb_wfs, dsp_config, verbosity=True)
    #peak_width(fom, 1, True)
    print(fom)

    fw[i], err[i] = fom
    flatDict[i] = flat
    riseDict[i] = rise






def main():
    conf_file = "../dspConfigFiles/downSampleTest.json"
    with open(conf_file) as f:
        dsp_config = json.load(f, object_pairs_hook=OrderedDict)
        
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    file = data["tier1_dir"] + "/opt"
    optSto = LH5Store(file)
    tb_wfs, nwfs = optSto.read_object('Card1/',"Run3.lh5")

    rise_arr = np.linspace(1,30,30)
    flat_arr = np.linspace(0.8,0.8,1)

    manager = mp.Manager()

    global fw, err, riseDict, flatDict
    fw = manager.dict()
    err = manager.dict()
    riseDict = manager.dict()
    flatDict = manager.dict()
    

    
    flat = 0.8
    for n in range(0, len(rise_arr)+1,4):
        print(n)
        try:
            p1 = mp.Process(target=noiseFit, args=(n,flat, rise_arr[n], dsp_config, tb_wfs))
            p1.start()
            n+=1
            p2 = mp.Process(target=noiseFit, args=(n,flat, rise_arr[n], dsp_config, tb_wfs))
            p2.start()
            n+=1
            p3 = mp.Process(target=noiseFit, args=(n,flat, rise_arr[n], dsp_config, tb_wfs))
            p3.start()
            n+=1
            p4 = mp.Process(target=noiseFit, args=(n,flat, rise_arr[n], dsp_config, tb_wfs))
            p4.start()
            n+=1
            p1.join()
            p2.join()
            p3.join()
            p4.join()

        except:
            continue

    df = pd.DataFrame({"FWHM": pd.Series(fw), "rise": pd.Series(riseDict), "flat": pd.Series(flatDict), "error": pd.Series(err)})
    df.to_csv("RiseNoiseChange1725lineSub.csv")







if __name__ == "__main__":
    main()