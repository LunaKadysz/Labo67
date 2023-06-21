# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 13:12:41 2023

@author: Luna
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

 
info_muestras = ms.pd.read_excel('data/info_muestras_1.xlsx')

for j,file in enumerate(ms.os.listdir('data/mediciones_nit')): #estoy diciendo que me recorra cada archivo de esa carpeta
    name = ms.os.path.splitext(file)[0]
    print(name)
    
    row = info_muestras[info_muestras['Nombre'] == name]
    muestra_i = ms.Muestra(name, row['Tipo'].iloc[0], row['Anillos'].iloc[0], row['Contactos'].iloc[0], row['Soldaduras'].iloc[0], row['Heater'].iloc[0])
    
    muestra_i.set_resistencias_mediciones_nit()
    
    if len(muestra_i.medicion_nit.R['R_avg'])>0:
        if muestra_i.tipo != 'Circular':
            f, (a0, a1) = plt.subplots(1, 2, figsize=(18,7), gridspec_kw={'width_ratios': [1, 3]})
            #plot contactos pares
            f.suptitle(f'{muestra_i.nombre} en nitrógeno',fontsize = 20)
            R_par = []
            x_ticks = []
            for i in range(1,int(muestra_i.contactos/2)):
                j =  int(muestra_i.contactos-i)
                print(f'({i},{j})')
                R_par_i_df = muestra_i.medicion_nit.R.loc[(muestra_i.medicion_nit.R['i']== i) & (muestra_i.medicion_nit.R['j']== j)]
                R_par_i = list(R_par_i_df['R_avg'])
                if len(R_par_i) >0:
                
                    R_par.append(R_par_i[0])
                    x_ticks.append(f'({i},{i}´)')
                
            a0.plot(R_par,'*',color='red',markersize=9,label='Contactos \n paralelos')
            
            a0.set_title('Resistencia transversal entre pares',fontsize = 15)
            a0.set(xticks=range(len(R_par)), xticklabels=x_ticks)
            a0.set_ylabel(r'$\rho_{xy}[k\Omega$]',fontsize = 15)
            a0.legend(fontsize = 15)
            a0.tick_params(axis='both', labelsize=14)
            
            #plot contactos i contra S y D
    
            S = int(muestra_i.contactos/2)
            D = int(muestra_i.contactos)
            
            df_D = muestra_i.medicion_nit.R[(muestra_i.medicion_nit.R['i']== D) | (muestra_i.medicion_nit.R['j']==D)].copy()
            df_S = muestra_i.medicion_nit.R[(muestra_i.medicion_nit.R['i']== S) | (muestra_i.medicion_nit.R['j']==S)].copy()   
            
            idD = (df_D['j'] == D)
            idS = (df_S['j'] == S)
            
            df_D.loc[idD,['i','j']] = df_D.loc[idD,['j','i']].values
            df_S.loc[idS,['i','j']] = df_S.loc[idS,['j','i']].values
            
            a1.axvline(S,color='black',label = f'Terminal S: {S}')
            a1.axvline(D,color='black',label = f'Terminal D: {D}')
            
            a1.plot(df_S['j'],df_S['R_avg'],'-o',label='$R_{S,i}$')
            a1.plot(df_D['j'],df_D['R_avg'],'-o',label='$R_{D,i}$')
            
            x_ticks1 = list(range(1,int(muestra_i.contactos/2)))
            x_ticks1_r = x_ticks1.copy()
            x_ticks1_r.reverse()
            x_ticks2 = [f"{i}'" for i in x_ticks1_r]
            x_ticks = x_ticks1 + ['S'] + x_ticks2 + ['D']
            a1.set(xticks=range(1,int(muestra_i.contactos)+1), xticklabels=x_ticks)
            a1.set_title('Resistencia longitudinal con S y D',fontsize = 15)
            a1.set_ylabel(r'$R[k\Omega$]',fontsize = 15)
            a1.legend(fontsize = 15)
            a1.set_xlabel('Contactos',fontsize = 15)
            a1.tick_params(axis='both', labelsize=14)
    # Create another legend for the second line.
        

        plt.savefig(f'figs/nitrogeno_2plots/{muestra_i.nombre}_amb.png', bbox_inches="tight")
 