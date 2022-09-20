import sys
import os
import io
import json
import argparse
import numpy as np
import pandas as pd
import h5py
from pprint import pprint
from collections import OrderedDict
import processes.foundation as fd
import matplotlib.pyplot as plt
from scipy import stats
from math import exp
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
from math import exp, sqrt, pi, erfc
from lmfit import Model
import csv

from pygama import flow
from pygama.raw.build_raw import build_raw
from pygama.dsp.build_dsp import build_dsp

def main():

    cwd = os.getcwd()
    file = cwd + '/coherent.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    config = cwd + '/../configFiles/config.json'
    with open(config, 'r') as read_file:
        configure = json.load(read_file)


    chan_file = cwd + "/../chan_config.json"
    conf_file = cwd + "/../dspConfigFiles/downSampleTest.json"
    with open(conf_file) as f:
        dsp = json.load(f, object_pairs_hook=OrderedDict)
    with open(chan_file) as f:
        chan_conf = json.load(f, object_pairs_hook=OrderedDict)

    fwMin = 100
    riseMin = 0
    flatMin = 0
    FW = []
    rise = []
    flat = []
    error = []
    runList = [x for x in range(8909,8931)]


    for i in range(4, 9):
        for j in np.arange(0.0,0.7, 0.1):

            dsp["processors"]["wf_trap"]["args"][1] = str(i) + '*us'
            dsp["processors"]["wf_trap"]["args"][2] = str(j) + '*us'

            json_object = json.dumps(dsp, indent=4)

        # Writing to sample.json
            with open(conf_file, "w") as outfile:
                outfile.write(json_object)

            for run in runList:
                dataFile = data['raw_dir'] + '/Run' + str(run) + '.lh5'
                outFile = data['dsp_dir'] + '/Run' + str(run) + '.lh5'

                build_dsp(dataFile, outFile, chan_config = chan_conf, write_mode = 'r')

            t2_data = fd.get_df_multiple(runList, 'Card1')

            c = 0.0408625
            m = -0.16892
            t2_data["calEnergy"] = t2_data["trapEmax"]*c + m 

            counts, bins, bars = plt.hist(t2_data['calEnergy'], histtype='step', bins=160000)

            lower = hA.find_nearest_bin(bins,160)
            upper = hA.find_nearest_bin(bins,190)
            ydata = counts[lower:upper]
            xdata = bins[lower:upper]
            l = np.argmax(ydata)

            gmodel = Model(fM.lingaus)
            #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
            params = gmodel.make_params(a1=1000, m1=xdata[l], s1=0.1, slope=-0.046, intrcpt=58)
            #params['s1'].vary = False
            result = gmodel.fit(ydata,params, x=xdata)

            sigma = result.params['s1'].value
            fw = 2.355*sigma
            try:
                FW.append(2.355*sigma)
                error.append(2.355*result.params['s1'].stderr)
                rise.append(i)
                flat.append(j)
            except:
                print('wierd')
            print(fw)
            print(i)
            print(j)


            if fw <= fwMin and fw >= 0:
                fwMin = fw
                riseMin = i
                flatMin = j



    dsp["processors"]["wf_trap"]["args"][1] = str(riseMin) + '*us'
    dsp["processors"]["wf_trap"]["args"][2] = str(flatMin) + '*us'
    print(fwMin)

    json_object = json.dumps(dsp, indent=4)

    df = pd.DataFrame({"rise":rise, "flat":flat, "FWHM":FW, "error":error})
    df.to_csv("noiseFit.csv")

# Writing to sample.json
    with open(conf_file, "w") as outfile:
        outfile.write(json_object)




if __name__ == "__main__":
    main()
