# -*- coding: utf-8 -*-
"""
Created on Mon May  8 08:50:17 2023

@author: DMC
"""
#import pandas as pd
#import numpy as np
import Muestras2 as ms
import matplotlib.pyplot as plt

path_abs = r'C:\Users\Luna\Documents\UBA\Labo6-7\Labo67\Labo6\Proyecto'
#path_abs = r'C:\Users\Usuario\Documents\luna_kadysz\Labo67\Labo6\Proyecto'
ms.os.chdir(path_abs)
#os.getcwd()

info_muestras = ms.pd.read_excel('data/info_muestras_1.xlsx')

 
for j,file in enumerate(ms.os.listdir('data/Mediciones1')): #estoy diciendo que me recorra cada archivo de esa carpeta
    name = ms.os.path.splitext(file)[0]
    
    row = info_muestras[info_muestras['Nombre'] == name]
    muestra_i = ms.Muestra(name, row['Tipo'].iloc[0], row['Anillos'].iloc[0], row['Contactos'].iloc[0], row['Soldaduras'].iloc[0], row['Heater'].iloc[0])
    
    muestra_i.set_resistencias()
    
    if len(muestra_i.R['R_avg'])>0:
        plt.figure()
        plt.plot(muestra_i.R['R_avg'])
    
#%% 
