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
    data = fd.get_t1_data(7032, "Card1")
    print(data[0]["accSum1"].nda)

    spec = np.zeros(len(data[0]["accSum1"].nda))
    for i in range(0, len(data[0]["accSum1"].nda)):
        value = 0.0
        for j in range(1,9):
            acc = "accSum" + str(j)
            hold = float(data[0][acc].nda[i]/100) - float(data[0]["accSum8"].nda[i]/300)
            value += hold
        spec[i] = value

    plt.hist(spec, histtype="step", bins = 30000)
    plt.show()


if __name__ == "__main__":
    main()