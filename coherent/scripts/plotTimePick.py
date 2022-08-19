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

    run = 3498
    t2_data = fd.get_df(3498, 'Card1')
    t1_data = fd.get_t1_data(3498)
    wf1 = t1_data["waveform"]["values"].nda[0]
    wf2 = t1_data["waveform"]["values"].nda[1]
    print(t2_data)

    plt.subplot(1,2,1)
    plt.axvline(t2_data["tp_max0"].loc[0]/8)
    plt.axvline((t2_data["tp_50"].loc[0]/8))
    plt.plot(wf1)
    plt.title("Plot of Waveform whose length has doubled")
    plt.ylabel("ADC")
    plt.xlabel("Clock ticks [8 ns]")
    plt.subplot(1,2,2)
    plt.axvline(t2_data["tp_max0"].loc[1]/8)
    plt.axvline((t2_data["tp_50"].loc[1]/8))
    plt.plot(wf2)
    plt.title("Plot of Waveform whose length has doubled")
    plt.ylabel("ADC")
    plt.xlabel("Clock ticks [8 ns]")
    plt.show()


if __name__ == "__main__":
    main()
