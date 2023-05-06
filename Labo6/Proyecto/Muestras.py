# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:40:22 2023

@author: Luna
"""

from itertools import combinations 
import pandas as pd
import numpy as np
import os

path_abs = r'C:\Users\Luna\Documents\UBA\Labo6-7\Labo67\Labo6\Proyecto'
os.chdir(path_abs)
#os.getcwd()

class Muestra:
  def __init__(self, nombre, tipo, anillos, contactos, soldaduras, heater, comentarios):
    self.nombre = nombre
    self.tipo = tipo
    self.soldaduras = soldaduras
    self.comentarios = comentarios
    
    #distintas atribuos para el tipo de muestra
    
    if self.tipo == "Circular": #muestras circulares
        self.anillos = anillos
        self.heater = heater
    else: # muestras rectangulares o cuadradas. 
        self.contactos = contactos
        self.R = {f'{i}': []   for i in list(combinations(range(1,self.contactos,2)))}
        self.R_error = {f'{i}': []   for i in list(combinations(range(1,self.contactos,2)))}
    #genero las resistencias
    
    def cargar_resistencias(self, nombre):
        #cargo el archivo donde tengo los valores de resistencia
        path = f'data/Mediciones1/{self.name}.csv'
        muestra = pd.read_csv(path, names=['i','j','R_min','R_max','R_avg'], header=None).drop(0).dropna()
        
        #cargo el archivo donde tengo la tabla de errores del multimetro
        df_error_multimetro = pd.read_csv('data/error_multimetro_R.csv')
        
        #cargo el archivo donde tengo las unidades de resistencia de cada muestra (ej: rango=ko,Mo,etc)
        df_rango = pd.read_csv('data/rango.csv')
        rango = list(df_rango[df_rango['nombre'] == self.nombre]['rango'])[0]
        
        for ij in self.R:
            R_ij = muestra[ij]['R_avg']
            self.R[ij] = R_ij
            
            #ahora construimos el error
            m,b = get_error_multimetro(df_error_multimetro,rango, R_ij) #llama a la funcion
            c_a = R_ij * m / 100 + b #error aparato
            c_b = (muestra[ij]['R_max'] - muestra[ij]['R_min'])/np.sqrt(100) #error estadistico
            self.R_error[ij] = c_a + c_b
            
    def get_error_multimetro(df,rango,R):
        #pongo como condicion que para que sea del rango 0< R/Rango <1
        df_error = df.loc[R/(df['Range']> 0) & (R/df['Range']< 1) & (df['Range2']== rango)]
        coefs = list(df_error['1 Year 23°C + 5°C'])[0].split('+')
        m = float(coefs[0])
        b = float(coefs[1])

        return m, b

