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

from pygama import flow
from pygama.raw.build_raw import build_raw
from pygama.dsp.build_dsp import build_dsp


def main():
    doc = ""
    rthf = argparse.RawTextHelpFormatter
    par = argparse.ArgumentParser(description=doc, formatter_class=rthf)
    arg, st, sf = par.add_argument, 'store_true', 'store_false'

    arg('-r', '--runs', nargs=1, type=str,
        help="list of files to process from runDB.json (-r #) ")
    arg('-c', '--config', nargs='*', type=str, help='configuration json file (-c config.json).')

    arg('--d2r', action=st, help='run daq_to_raw')
    arg('--r2d', action=st, help='run raw_to_dsp')

    args = par.parse_args()

    run = args.runs[0]
    config_file = args.config[0]

    cwd = os.getcwd()
    file = cwd + '/coherent.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    config = cwd + '/' + config_file
    with open(config, 'r') as read_file:
        configure = json.load(read_file)



    dataFile = data['daq_dir'] + str(run)
    outFile = data['raw_dir'] + str(run) + '.lh5'
    configure["ORSIS3316WaveformDecoder"]["Card1"]["out_stream"] = outFile
    configure["ORiSegHVCardDecoderForHV"]["HV1"]["out_stream"] = outFile
    configure["ORCAEN792NDecoderForQdc"]["QDC"]["out_stream"] = outFile

    build_raw(dataFile, data['stream_type'], configure, overwrite=True)


if __name__ == "__main__":
    main()
