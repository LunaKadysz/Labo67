# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:49:17 2023

@author: DMC
"""

import numpy as np
import pandas as pd

df = pd.read_csv("data/20230626104041.txt", sep="\t")


#%%

import matplotlib.pyplot as plt
plt.figure()
plt.plot(df['# frequency (Hz)'],df['Voltage_X (V) '],'-o', label='X')
plt.plot(df['# frequency (Hz)'],np.abs(df['Voltage_Y (V)']),'-o', label='Y')
plt.xscale('log')
plt.show()
plt.legend()
