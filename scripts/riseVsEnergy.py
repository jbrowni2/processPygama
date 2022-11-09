import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
from scipy import signal
from math import exp
import processes.foundation as fd
from math import exp, sqrt, pi, erfc
from lmfit import Model
import csv
from scipy.optimize import curve_fit
import pywt
from statistics import median
import copy


def find_idx(arr, val, idxBegin):
        for i in range(idxBegin, 0, -1):
            count = arr[i]
            if count <= val:
                break

        idx = i
        return idx


def find_idxr(arr, val, idxBegin):
        for i in range(idxBegin, len(arr)-1, 1):
            count = arr[i]
            if count >= val:
                break
        
        idx = i
        return idx








def main():
    run_list = [x for x in range(1367,1380)]
    df = fd.get_df_multiple(run_list, "Card1")
    rise_time = np.zeros(len(df["timestamp"]))
    
    m = 0
    for run in run_list:
        data = fd.get_t1_data(run, "Card1")

        for n, wave in enumerate(data[0]["waveform"]["values"].nda):
            cDs = pywt.swt(wave, "haar", level=4)
            threshold = np.zeros_like([0,0,0,0])

            j=0
            for cD in cDs:
                median_value = median(cD[1])
                median_average_deviation = median([abs(number-median_value) for number in cD[1]])
                sig1 = median_average_deviation/0.6745
                threshold[j] = sig1*np.sqrt(2*np.log(len(wave)))
                j+=1

            j=0
            for cD in cDs:
                cD[1][abs(cD[1]) < threshold[j]] = 0.0
                j += 1

            wave = pywt.iswt(cDs, "Haar")

            mean = np.nan
            stdev = np.nan
            slope = np.nan
            intercept = np.nan


            sum_x = sum_x2 = sum_xy = sum_y = mean = stdev = 0
            isum = 15000

            for i in range(0, 15000, 1):
            # the mean and standard deviation
                temp = wave[i] - mean
                mean += temp / (i + 1)
                stdev += temp * (wave[i] - mean)

                # linear regression
                sum_x += i
                sum_x2 += i * i
                sum_xy += wave[i] * i
                sum_y += wave[i]

            slope = (isum * sum_xy - sum_x * sum_y) / (isum * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - sum_x * slope) / isum

            line = np.array([x * slope + intercept for x in range(0, len(wave))])
            wave = wave - line

            max = np.mean(wave[17000:20000])
            min = np.amin(wave)
            m90 = max*0.9
            m10 = max*0.1
            m50 = max*0.5
            imax51 = find_idx(wave, m50, 17000)
            imax9 = find_idxr(wave, m90, imax51)
            imax1 = find_idx(wave, m10, imax51)
            rise_time[m] = imax9 - imax1
            m += 1

    df["energy"] = df["trapEmax"]*0.0408625 -0.16892

    plt.hist2d(df["energy"], rise_time, bins=(400,1000), cmap=plt.cm.Greys)
    plt.ylim(10,100)
    plt.xlim(10,1000)
    plt.show()



if __name__ == "__main__":
    main()