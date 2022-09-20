import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from math import exp
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
from math import exp, sqrt, pi, erfc
from lmfit import Model


def main():

    m = 2
    b = -1
    arr = np.ndarray([x*m + b for x in range(0,2000)])
    print(arr)




if __name__ == "__main__":
    main()