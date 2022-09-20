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
    t1_data = fd.get_t1_data(8651, "Card1")
    wf = t1_data[0]["waveform"]["values"].nda[0]
    

    #here we took 3 as our input
    n = 10
  
    # calculates the average
    avgResult = np.average(wf.reshape(-1, n), axis=1)
  
    print("Given array:")
    print(wf)
  
    print("Averaging over every ", n, " elements of a numpy array:")
    print(avgResult)
    



if __name__ == "__main__":
    main()