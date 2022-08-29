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
    t1_data = fd.get_t1_data(1193, 'HV1')
    print(t1_data)



if __name__ == "__main__":
    main()
