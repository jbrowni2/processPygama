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
    t2_data = fd.get_df(1035, "Card1")
    energy = [(t2_data["maxEnergy"].loc[i] - t2_data["startEnergy"].loc[i]) for i in range(0,len(t2_data["startEnergy"]))]

    plt.subplot(1,2,2)
    plt.hist(energy, histtype="step", bins = 2000000)
    plt.show()



if __name__ == "__main__":
    main()
