import matplotlib.pyplot as plt
import numpy as np
import h5py 
import copy
from collections import OrderedDict

import os
import pygama
import pygama.lgdo as lgdo
import pygama.lgdo.lh5_store as lh5

from pygama.lgdo.lh5_store import LH5Store
from pygama.lgdo.table import Table
from pygama.lgdo.arrayofequalsizedarrays import ArrayOfEqualSizedArrays
from pygama.lgdo.array import Array
import processes.foundation as fd
import argparse

doc = ""
rthf = argparse.RawTextHelpFormatter
par = argparse.ArgumentParser(description=doc, formatter_class=rthf)
arg, st, sf = par.add_argument, 'store_true', 'store_false'

arg('-r', '--runs', nargs=1, type=int,
            help="list of files to process from runDB.json (-r #) ")

args = par.parse_args()

run = args.runs[0]

raw_dir = "/home/jlb1694/data/raw"
sto = LH5Store(raw_dir)

lh5_keys = fd.get_tables(run)
OldF = "Run" + str(run) + '.lh5'
BackF = "Run" + str(run) + 'Backround.lh5'
sigF = "Run" + str(run) + 'Signal.lh5'

N = 5
for tb in lh5_keys:

    tb_wfs, nwfs = sto.read_object(tb+'/',[OldF])
    if tb == "HV1":
        sto.write_object(tb_wfs,tb,BackF)
        continue
    elif tb == "HV2":
        sto.write_object(tb_wfs,tb,BackF)
        continue
    elif tb == "LN":
        sto.write_object(tb_wfs,tb,BackF)
        continue
    elif tb == "LN":
        sto.write_object(tb_wfs,tb,BackF)
        continue

    tb_wfs.resize(nwfs*N)

    tb_timestamps = tb_wfs['timestamp'].nda
    waveform_values = tb_wfs['waveform']['values'].nda
    waveform_t0 = tb_wfs['waveform']['t0'].nda
    waveform_dt = tb_wfs['waveform']['dt'].nda
    waveform_pretrig = tb_wfs["preTrigger"].nda

    len_wf = len(waveform_values[0])
    sig_arr = np.zeros((nwfs, int(len_wf/N)))
    sig_times = np.zeros(nwfs)
    reshape = (N*nwfs,int(len_wf/N))
    back_arr = np.zeros(reshape)
    back_times = np.zeros(N*nwfs)

    for i in range(nwfs):
        wf = waveform_values[i]
        original_t0 = tb_timestamps[i]
        pretrigger = waveform_pretrig[i]

        for j in range(N):
            idx = N*i + j

            start = j*(int(len_wf/N))
            stop = (j+1)*(int(len_wf/N))
            if start < pretrigger and stop > pretrigger:
                sig_arr[i] = wf[start:stop]
                new_timestamp = original_t0 - (int(pretrigger) - int(j*(len_wf/N)))
                sig_times[i] = new_timestamp
            else:
                back_arr[idx] = wf[start:stop]

                new_timestamp = original_t0 - (int(pretrigger) - int(j*(len_wf/N)))
                back_times[idx] = new_timestamp



    new_values = ArrayOfEqualSizedArrays(reshape,back_arr,back_arr.shape,fill_val=back_arr)
    tb_wfs['waveform']['values'] = new_values

    new_t0 = Array(back_times,back_times.shape,attrs={'units': 'ns'})
    tb_wfs['waveform']['t0'] = new_t0

    sto.write_object(tb_wfs,tb,BackF)

    new_values = ArrayOfEqualSizedArrays((nwfs, int(len_wf/N)),sig_arr,sig_arr.shape,fill_val=sig_arr)
    tb_wfs['waveform']['values'] = new_values

    new_t0 = Array(sig_times,sig_times.shape,attrs={'units': 'ns'})
    tb_wfs['waveform']['t0'] = new_t0

    sto.write_object(tb_wfs,tb,sigF)