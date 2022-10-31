import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from scipy import signal
from math import exp
import processes.foundation as fd
from math import exp, sqrt, pi, erfc
from lmfit import Model
import csv

def main():
    run_list = [x for x in range(1364,1366)]
    t2_data1 = fd.get_df_multiple(run_list, "Card1")
    run_list = [x for x in range(1367,1388)]
    t2_data2 = fd.get_df_multiple(run_list, "Card1")
    run_list = [x for x in range(1390,1396)]
    t2_data3 = fd.get_df_multiple(run_list, "Card1")
    t2_data = pd.concat([t2_data1, t2_data2, t2_data3])
    c = 0.0428
    m = -0.193
    t2_data["calEnergy"] = t2_data["trapEmax"]*c + m 

    #plt.subplot(1,2,2)
    plt.hist(t2_data['calEnergy'], histtype="step", bins = 320000)
    #plt.xlim(0,1500)
    #plt.ylim(0,5000)
    plt.yscale('log')
    plt.show()



if __name__ == "__main__":
    main()
