import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import processes.foundation as fd
import plotly.express as px
import sys


def main():

    runs = [x for x in range(3454,3499)]
    t2_data = fd.get_df_multiple(runs, 'Card1')
    dt = []

    for i in range(1, len(t2_data["tp_50"])-1):
        if t2_data["channel"].loc[i] == 9 and t2_data["channel"].loc[i+1] == 11:
            time1 = (t2_data["tp_50"].loc[i])
            time2 = (t2_data["tp_50"].loc[i+1])
            dt.append(time2-time1)

    plt.hist(dt, histtype='step', bins=3000)
    plt.xlim(0,2000)
    plt.xlabel("ns")
    plt.show()




if __name__ == "__main__":
    main()
