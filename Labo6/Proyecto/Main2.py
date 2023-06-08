# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:43:04 2023

@author: Luna
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
        plt.figure(figsize=(18,13))
        plt.title(f'{muestra_i.nombre} Ambiente',fontsize = 20)
        plt.xlabel('$R_i$',fontsize = 20)
        plt.ylabel('R[$k\Omega$]',fontsize = 20)
        plt.xticks(range(1,int(muestra_i.contactos)+1),fontsize = 15)
        plt.yticks(fontsize = 15)
        #plt.plot(muestra_i.R['R_avg'])
        plot_lines2 = []
        rango = range(muestra_i.medicion_amb.R['i'].min(),muestra_i.medicion_amb.R['j'].max()+1)
        for i in rango:
            df_i = muestra_i.medicion_amb.R[(muestra_i.medicion_amb.R['i']==i) | (muestra_i.medicion_amb.R['j']==i)].copy()
    
            idx = (df_i['j'] == i)
            #df_i = muestra.medicion_nit.R[muestra.medicion_nit.R['i']==i]
            #df_j = muestra.medicion_nit.R[muestra.medicion_nit.R['j']==i]
            df_i.loc[idx,['i','j']] = df_i.loc[idx,['j','i']].values
            if len(df_i) >0:
                p, = plt.plot(df_i['j'],df_i['R_avg'],'-o',label=f'R_i,{i}',linewidth= 2, markersize=4)
                #plt.errorbar(range(i,len(df_i)+i),df_i['R_avg'],yerr=df_i['R_error'],fmt='-o',label=f'{i}')
                plot_lines2.append(p)
                
        a = plt.axvline(muestra_i.contactos/2,color='black',label=f'Contacto {int(muestra_i.contactos/2)}')
        b = plt.axvline(muestra_i.contactos,color='black',label=f'Contacto {int(muestra_i.contactos)}')
        plot_lines1 = [a,b]
        # Create a legend for the first line.
        first_legend = plt.legend(handles=plot_lines2, loc='best',fontsize = 15)

        # Add the legend manually to the current Axes.
        ax = plt.gca().add_artist(first_legend)

# Create another legend for the second line.
        plt.legend(handles=plot_lines1, loc=2,fontsize = 15)

        #plt.savefig(f'figs/intento2/{muestra_i.nombre}_amb.png', bbox_inches="tight", pad_inches = 0)
    
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
        if muestra_i.tipo != 'Circular':
            plt.figure(figsize=(18,13))
            plt.title(f'{muestra_i.nombre} Nitrogeno',fontsize = 20)
            plt.xlabel('$R_i$',fontsize = 20)
            plt.ylabel('R[$k\Omega$]',fontsize = 20)
            plt.xticks(range(1,int(muestra_i.contactos)+1),fontsize = 15)
            plt.yticks(fontsize = 15)
            #plt.plot(muestra_i.R['R_avg'])
            plot_lines2 = []
    
            #plt.plot(muestra_i.R['R_avg'])
            #solo vale en cuadradas: 
        
            rango = range(muestra_i.medicion_nit.R['i'].min(),muestra_i.medicion_nit.R['j'].max()+1)
            for i in rango:
                df_i = muestra_i.medicion_nit.R[(muestra_i.medicion_nit.R['i']==i) | (muestra_i.medicion_nit.R['j']==i)].copy()
        
                idx = (df_i['j'] == i)
                #df_i = muestra.medicion_nit.R[muestra.medicion_nit.R['i']==i]
                #df_j = muestra.medicion_nit.R[muestra.medicion_nit.R['j']==i]
                df_i.loc[idx,['i','j']] = df_i.loc[idx,['j','i']].values
                if len(df_i) >0:
                    p, = plt.plot(df_i['j'],df_i['R_avg'],'-o',label=f'R_i,{i}',linewidth= 2, markersize=4)
                    #plt.errorbar(range(i,len(df_i)+i),df_i['R_avg'],yerr=df_i['R_error'],fmt='-o',label=f'{i}')
                    plot_lines2.append(p)
                    
            a = plt.axvline(muestra_i.contactos/2,color='black',label=f'Contacto {int(muestra_i.contactos/2)}')
            b = plt.axvline(muestra_i.contactos,color='black',label=f'Contacto {int(muestra_i.contactos)}')
            plot_lines1 = [a,b]
            # Create a legend for the first line.
            first_legend = plt.legend(handles=plot_lines2, loc='best',fontsize = 15)
    
            # Add the legend manually to the current Axes.
            ax = plt.gca().add_artist(first_legend)
    
    # Create another legend for the second line.
            plt.legend(handles=plot_lines1, loc=2,fontsize = 15)
    
            #plt.savefig(f'figs/intento2/{muestra_i.nombre}_nit.png')