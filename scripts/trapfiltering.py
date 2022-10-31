import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.signal as sig


t1_data = fd.get_t1_data(1397, "Card1")

rise = int(8*1000/8)
flat = int(0.5*1000/8)

trapFilter = np.zeros(2*rise + flat)

trapFilter[0:rise] = 1.0
trapFilter[rise+1:flat+rise] = 0.0
trapFilter[rise+flat+1:] = -1.0


trapWave = np.zeros((len(t1_data[0]["waveform"]["values"].nda), len(t1_data[0]["waveform"]["values"].nda[0])- len(trapFilter)+1))
for i,wave in enumerate(t1_data[0]["waveform"]["values"].nda):
    trapWave[i] = sig.convolve(wave, trapFilter, "valid")


#plt.plot(df.iloc[0])
#plt.plot(trap)
plt.plot(trapWave[10])
plt.plot()
plt.show()


"""
rise = int(8*1000/8)
flat = int(0.8*1000/8)

for i in range(1, rise, 1):
    df.iloc[0][i] = df.iloc[0][i - 1] + df.iloc[0][i]
for i in range(rise, rise + flat, 1):
    df.iloc[0][i] = df.iloc[0][i - 1] + df.iloc[0][i] - df.iloc[0][i - rise]
for i in range(rise + flat, 2 * rise + flat, 1):
    df.iloc[0][i] = df.iloc[0][i - 1] + df.iloc[0][i] - df.iloc[0][i - rise] - df.iloc[0][i - rise - flat]
for i in range(2 * rise + flat, len(df.iloc[0]), 1):
    df.iloc[0][i] = (
            df.iloc[0][i - 1]
            + df.iloc[0][i]
            - df.iloc[0][i - rise]
            - df.iloc[0][i - rise - flat]
            + df.iloc[0][i - 2 * rise - flat])
            

plt.plot(df.iloc[0])
plt.show()

"""