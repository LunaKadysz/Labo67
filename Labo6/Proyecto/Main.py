# -*- coding: utf-8 -*-
"""
Created on Mon May  8 08:50:17 2023

@author: DMC
"""
#import pandas as pd
#import numpy as np
import Muestras2 as ms
import matplotlib.pyplot as plt

#path_abs = r'C:\Users\Luna\Documents\UBA\Labo6-7\Labo67\Labo6\Proyecto'
path_abs = r'C:\Users\Usuario\Documents\luna_kadysz\Labo67\Labo6\Proyecto'
ms.os.chdir(path_abs)
#os.getcwd()
#%%
info_muestras = ms.pd.read_excel('data/info_muestras_1.xlsx')

 
for j,file in enumerate(ms.os.listdir('data/mediciones_amb')): #estoy diciendo que me recorra cada archivo de esa carpeta
    name = ms.os.path.splitext(file)[0]
    print(name)
    row = info_muestras[info_muestras['Nombre'] == name]
    muestra_i = ms.Muestra(name, row['Tipo'].iloc[0], row['Anillos'].iloc[0], row['Contactos'].iloc[0], row['Soldaduras'].iloc[0], row['Heater'].iloc[0])
    
    muestra_i.set_resistencias_mediciones_amb()
    
    if len(muestra_i.medicion_amb.R['R_avg'])>0:
        plt.figure()
        plt.title(f'{muestra_i.nombre} Ambiente')
        plt.xlabel('$R_i$')
        plt.ylabel('R[$k\Omega$]')
        #plt.plot(muestra_i.R['R_avg'])
        for i in range(muestra_i.medicion_amb.R['i'].min(),muestra_i.medicion_amb.R['i'].max()+1):
            df_i = muestra_i.medicion_amb.R[muestra_i.medicion_amb.R['i']==i]
            if len(df_i) >0:
                plt.plot(df_i['j'],df_i['R_avg'],'-o',label=f'{i}')
                #plt.errorbar(range(i,len(df_i)+i),df_i['R_avg'],yerr=df_i['R_error'],fmt='-o',label=f'{i}')
                plt.legend()
        plt.savefig(f'figs/{muestra_i.nombre}_amb.png')
    
#%% 

import Muestras2 as ms
import matplotlib.pyplot as plt

info_muestras = ms.pd.read_excel('data/info_muestras_1.xlsx')

for j,file in enumerate(ms.os.listdir('data/mediciones_nit')): #estoy diciendo que me recorra cada archivo de esa carpeta
    name = ms.os.path.splitext(file)[0]
    print(name)
    
    row = info_muestras[info_muestras['Nombre'] == name]
    muestra_i = ms.Muestra(name, row['Tipo'].iloc[0], row['Anillos'].iloc[0], row['Contactos'].iloc[0], row['Soldaduras'].iloc[0], row['Heater'].iloc[0])
    
    muestra_i.set_resistencias_mediciones_nit()
    
    if len(muestra_i.medicion_nit.R['R_avg'])>0:
        plt.figure()
        plt.title(f'{muestra_i.nombre} Nitrogeno')
        plt.xlabel('$R_i$')
        plt.ylabel('R[$k\Omega$]')
        #plt.plot(muestra_i.R['R_avg'])
        #solo vale en cuadradas: 
        if muestra_i.tipo != 'Circular':
            for i in range(muestra_i.medicion_nit.R['i'].min(),muestra_i.medicion_nit.R['i'].max()+1):
                df_i = muestra_i.medicion_nit.R[muestra_i.medicion_nit.R['i']==i]
                if len(df_i) >0:
            
                    plt.plot(df_i['j'],df_i['R_avg'],'-o',label=f'{i}')
                    #plt.errorbar(range(i,len(df_i)+i),df_i['R_avg'],yerr=df_i['R_error'],fmt='-o',label=f'{i}')
                    plt.legend()
        plt.savefig(f'figs/{muestra_i.nombre}_nit.png')
                
        """
        #df = muestra_i.medicion_nit.R
        """
        plt.show()