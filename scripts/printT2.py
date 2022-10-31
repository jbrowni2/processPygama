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
    t2_data = fd.get_t1_data(7032, "Card1")
    print(t2_data[0]["accSum1"].nda)



if __name__ == "__main__":
    main()
