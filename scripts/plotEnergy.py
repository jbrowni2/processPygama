import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from math import exp
import processes.foundation as fd
from math import exp, sqrt, pi, erfc
from lmfit import Model
import csv

def main():
    run_list = [x for x in range(1202,1207)]
    t2_data = fd.get_df_multiple(run_list, "Card1")
    #energy = [(t2_data["maxEnergy"].loc[i] - t2_data["startEnergy"].loc[i]) for i in range(0,len(t2_data["startEnergy"]))]

    #plt.subplot(1,2,2)
    plt.hist(t2_data['trapEmax'], histtype="step", bins = 200000)
    plt.xlim(0,1000)
    plt.show()



if __name__ == "__main__":
    main()
