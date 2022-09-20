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
    run_list = [x for x in range(8662,8684)]
    t2_data = fd.get_df_multiple(run_list, "Card1")
    c = 0.0408625
    m = -0.16892
    t2_data["calEnergy"] = t2_data["trapEmax"]*c + m 

    #plt.subplot(1,2,2)
    plt.hist(t2_data['calEnergy'], histtype="step", bins = 320000)
    plt.xlim(58,59)
    plt.ylim(0,400)
    plt.show()



if __name__ == "__main__":
    main()
