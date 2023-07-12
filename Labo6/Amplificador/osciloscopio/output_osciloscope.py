# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:34:35 2023

@author: DMC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

data = {}

for j,file in enumerate(os.listdir('data')): #estoy diciendo que me recorra cada archivo de esa carpeta
	name = os.path.splitext(file)[0]
	ext = os.path.splitext(file)[1]
	
	
	ch = name.split('_')[0]
	freq = name.split('_')[1]
	
	if ext == 'npy':
		data[freq]['info'][ch] =  file # este archivo contiene la info de la medicio (vdiv, tdiv, etc)
		
	else:
		data[freq][ch] = file
		
		