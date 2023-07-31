# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:03:26 2023

@author: DMC
"""

#import pandas as pd
#import numpy as np

import matplotlib.pyplot as plt
import Muestras2 as ms

path_abs = r'C:\Users\Luna\Documents\UBA\Labo6-7\Labo67\Labo6\Proyecto'
#path_abs = r'C:\Users\Usuario\Documents\luna_kadysz\Labo67\Labo6\Proyecto'
ms.os.chdir(path_abs)
#os.getcwd()


#%%

info_muestras = ms.pd.read_excel('data/info_muestras_1.xlsx')

name = 'PTB-P733-10'
row = info_muestras[info_muestras['Nombre'] == name]
muestra = ms.Muestra(name, row['Tipo'].iloc[0], row['Anillos'].iloc[0], row['Contactos'].iloc[0], row['Soldaduras'].iloc[0], row['Heater'].iloc[0])
    
muestra.set_resistencias_mediciones_amb()
    

f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 2]})

#plot contactos pares
R_par = []
x_ticks = []
for i in range(1,int(muestra.contactos/2)):
    j =  int(muestra.contactos-i)
    print(f'({i},{j})')
    R_par_i_df = muestra.medicion_amb.R.loc[(muestra.medicion_amb.R['i']== i) & (muestra.medicion_amb.R['j']== j)]
    R_par_i = list(R_par_i_df['R_avg'])
    if len(R_par_i) >0:
    
        R_par.append(R_par_i[0])
        x_ticks.append(f'({i},{i}´)')
    
a0.set_title(f'{muestra.nombre} ambiente',fontsize = 20)
a0.plot(R_par,'o',label='Contactos paralelos')
a0.set(xticks=range(len(R_par)), xticklabels=x_ticks)
a0.set_ylabel(r'$\rho_{xy}[k\Omega$]',fontsize = 15)
a0.legend()


#plot contactos i contra S y D

S = int(muestra.contactos/2)
D = int(muestra.contactos)

df_D = muestra.medicion_amb.R[(muestra.medicion_amb.R['i']== D) | (muestra.medicion_amb.R['j']==D)].copy()
df_S = muestra.medicion_amb.R[(muestra.medicion_amb.R['i']== S) | (muestra.medicion_amb.R['j']==S)].copy()   

idD = (df_D['j'] == D)
idS = (df_S['j'] == S)

df_D.loc[idD,['i','j']] = df_D.loc[idD,['j','i']].values
df_S.loc[idS,['i','j']] = df_S.loc[idS,['j','i']].values

a1.axvline(S,color='black',label = f'Terminal S: {S}')
a1.axvline(D,color='black',label = f'Terminal D: {D}')

a1.plot(df_S['j'],df_S['R_avg'],'-o',label='$R_{S,i}$')
a1.plot(df_D['j'],df_D['R_avg'],'-o',label='$R_{D,i}$')

a1.set_ylabel(r'$R[k\Omega$]',fontsize = 15)
a1.legend()



# ploteos: error de los contactos y perdida longitudinal.
# para la longitudinal tener en cuaenta el error por fem (cambiar la polarizacion y promediar)

