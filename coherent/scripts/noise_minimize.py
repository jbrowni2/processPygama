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

    config = cwd + '/config.json'
    with open(config, 'r') as read_file:
        configure = json.load(read_file)


    chan_file = cwd + "/chan_config.json"
    conf_file = cwd + "/dsp_config.json"
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


    for i in range(6, 13):
        for j in np.arange(0.3,1.2, 0.1):

            dsp["processors"]["wf_trap"]["args"][1] = str(i) + '*us'
            dsp["processors"]["wf_trap"]["args"][2] = str(j) + '*us'

            json_object = json.dumps(dsp, indent=4)

        # Writing to sample.json
            with open(conf_file, "w") as outfile:
                outfile.write(json_object)


            dataFile = data['raw_dir'] + '/Run1124.lh5'
            outFile = data['dsp_dir'] + '/Run1124.lh5'

            build_dsp(dataFile, outFile, chan_config = chan_conf, write_mode = 'r')

            t2_data = fd.get_df(1124, 'Card1')

            counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)

            lower = fd.find_nearest_bin(bins,50)
            upper = fd.find_nearest_bin(bins,120)
            ydata = counts[lower:upper]
            xdata = bins[lower:upper]
            l = np.argmax(ydata)

            gmodel = Model(fd.lingaus)
            #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
            params = gmodel.make_params(a1=1000, m1=xdata[l], s1=2.0, slope=-0.046, intrcpt=58)
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

            if fw <= fwMin and fw >= 0:
                fwMin = fw
                riseMin = i
                flatMin = j



    dsp["processors"]["wf_trap"]["args"][1] = str(riseMin) + '*us'
    dsp["processors"]["wf_trap"]["args"][2] = str(flatMin) + '*us'
    print(fwMin)

    json_object = json.dumps(dsp, indent=4)

# Writing to sample.json
    with open(conf_file, "w") as outfile:
        outfile.write(json_object)

    with open('noiseFit', 'w') as f:

        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(rise)
        write.writerow(flat)
        write.writerow(FW)
        write.writerow(error)




if __name__ == "__main__":
    main()
