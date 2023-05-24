# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:40:22 2023

@author: Luna
"""

from itertools import combinations 
import pandas as pd
import numpy as np
import os

#path_abs = r'C:\Users\Luna\Documents\UBA\Labo6-7\Labo67\Labo6\Proyecto'
path_abs = r'C:\Users\Usuario\Documents\luna_kadysz\Labo67\Labo6\Proyecto'
os.chdir(path_abs)
#os.getcwd()
#%%
class Muestra:
    def __init__(self, nombre, tipo, anillos, contactos, soldaduras, heater):
        self.nombre = nombre
        self.tipo = tipo
        self.soldaduras = soldaduras
        
        #distintas atribuos para el tipo de muestra
        
        if self.tipo == "Circular": #muestras circulares
            self.anillos = anillos
            self.heater = heater
        else: # muestras rectangulares o cuadradas. 
            self.contactos = contactos

        #genero las resistencias
    
    def set_resistencias_mediciones_amb(self):
        """
        Esta funcion le carga a cada instancia de muestra
        las resistencias medidas a temperatura ambiente

        """
        self.medicion_amb = type("medicion", (),{})()
        
        #cargo el archivo donde tengo los valores de resistencia
        path = f'data/mediciones_amb/{self.nombre}.csv'
        muestra = pd.read_csv(path, names=['i','j','R_min','R_max','R_avg'], header=None).drop(0).dropna().reset_index()
        
        #aca emprolijo la notacion de indices: (i -> i, j) -> j como enteros
        muestra['i'] = [int(ind.split('(')[1]) for ind in muestra['i']]
        muestra['j'] = [int(ind.split(')')[0]) for ind in muestra['j']]
        
        #cargo el archivo donde tengo la tabla de errores del multimetro
        df_error_multimetro = pd.read_csv('data/error_multimetro_R.csv')
        
        #cargo el archivo donde tengo las unidades de resistencia de cada muestra (ej: rango=ko,Mo,etc)
        df_rango = pd.read_csv('data/rango.csv')
        rango = list(df_rango[df_rango['nombre'] == self.nombre]['rango'])[0]
        
        #atributo de resistencia
        muestra['R_error'] = [self.get_error_multimetro(df_error_multimetro, muestra, i, R, rango) for i,R in enumerate(muestra['R_avg'])] 
        self.medicion_amb.R = muestra




    def set_resistencias_mediciones_nit(self):
            """
            Esta funcion le carga a cada instancia de muestra
            las resistencias medidas a temperatura ambiente
    
            """
            self.medicion_nit = type("medicion", (),{})()
            
            #cargo el archivo donde tengo los valores de resistencia
            path = f'data/mediciones_nit/{self.nombre}.csv'
            #muestra = pd.read_csv(path, names=['i','j','R_avg','R_min','R_max'], header=None).drop(0).dropna().reset_index()
            muestra = pd.read_csv(path).drop(0).dropna().reset_index()
            
            muestra[['R_avg','R_min','R_max']] = muestra[['R_avg','R_min','R_max']]/1000
            
            #limpio los ovld
            muestra = muestra[muestra['R_avg']<1000].dropna().reset_index()

            #aca emprolijo la notacion de indices: (i -> i, j) -> j como enteros
            muestra['i'] = [int(ind) for ind in muestra['i']]
            muestra['j'] = [int(ind) for ind in muestra['j']]
            
            #cargo el archivo donde tengo la tabla de errores del multimetro
            df_error_multimetro = pd.read_csv('data/error_multimetro_R.csv')
            
            #cargo el archivo donde tengo las unidades de resistencia de cada muestra (ej: rango=ko,Mo,etc)
            df_rango = pd.read_csv('data/rango.csv')
            rango = list(df_rango[df_rango['nombre'] == self.nombre]['rango'])[0]
            
            #atributo de resistencia
            muestra['R_error'] = [self.get_error_multimetro(df_error_multimetro, muestra, i, R, rango) for i,R in enumerate(muestra['R_avg'])] 
            self.medicion_nit.R = muestra




    def get_error_multimetro(self,df_e, muestra,i,R,rango):
        """
        Esta funcion se usa dentro del metodo del metodo que carga resistencias a 
        temperatura ambiente para asignarle el error a cada medicion.

        """
        
        #pongo como condicion que para que sea del rango 0< R/Rango <1
        df_error = df_e[((R/df_e['Range'])> 1/1000) & ((R/df_e['Range'])< 1) & (df_e['Range2']== f' {rango}')]
        coefs = list(df_error['1 Year 23°C + 5°C'])[0].split('+')
        m = float(coefs[0])
        b = float(coefs[1])
        c_a = R * m / 100 + b #error aparato
        c_b = (float(muestra['R_max'][i]) - float(muestra['R_min'][i]))/np.sqrt(100) #error estadistico
        return c_a + c_b
    
        