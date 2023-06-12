# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 10:28:25 2023

@author: Luna
"""
#import pandas as pd
#import numpy as np

import matplotlib.pyplot as plt
import Muestras2 as ms

#path_abs = r'C:\Users\Luna\Documents\UBA\Labo6-7\Labo67\Labo6\Proyecto'
path_abs = r'C:\Users\Usuario\Documents\luna_kadysz\Labo67\Labo6\Proyecto'
ms.os.chdir(path_abs)
#os.getcwd()


#%%

info_muestras = ms.pd.read_excel('data/info_muestras_1.xlsx')

row = info_muestras[info_muestras['Nombre'] == 'ULF-A1A2']
muestra = ms.Muestra('ULF-A1A2', row['Tipo'].iloc[0], row['Anillos'].iloc[0], row['Contactos'].iloc[0], row['Soldaduras'].iloc[0], row['Heater'].iloc[0])
    
muestra.set_resistencias_mediciones_amb()
    
plt.figure(figsize=(18,13))
plt.title(f'{muestra.nombre} Amb',fontsize = 20)
plt.xlabel('$R_i$',fontsize = 20)
plt.ylabel('R[$k\Omega$]',fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
for i in range(muestra.medicion_amb.R['i'].min(),muestra.medicion_amb.R['j'].max()+1):

    df_i = muestra.medicion_amb.R[(muestra.medicion_amb.R['i']==i) | (muestra.medicion_amb.R['j']==i)].copy()
    print(df_i)
    idx = (df_i['j'] == i)
    #df_i = muestra.medicion_nit.R[muestra.medicion_nit.R['i']==i]
    #df_j = muestra.medicion_nit.R[muestra.medicion_nit.R['j']==i]
    df_i.loc[idx,['i','j']] = df_i.loc[idx,['j','i']].values
    print(df_i)
    if len(df_i) >0:
        plt.plot(df_i['j'],df_i['R_avg'],'-o',label=f'R_{i},i')
                #plt.errorbar(range(i,len(df_i)+i),df_i['R_avg'],yerr=df_i['R_error'],fmt='-o',label=f'{i}')
        
plt.axvline(muestra.contactos/2,color='black',label = f'Terminal {muestra.contactos/2}')
plt.axvline(muestra.contactos,color='black',label = f'Terminal {muestra.contactos}')
plt.legend(fontsize = 15)
plt.savefig("figs/prueba.png")