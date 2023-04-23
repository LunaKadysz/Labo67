# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:40:22 2023

@author: Luna
"""

from itertools import combinations 
import pandas as pd
import numpy as np


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
    
    def cargar_resistencias(self, archivo):
        muestra = archivo[self.nombre]
        
        for ij in self.R:
            R_ij = muestra[ij]['R_avg']
            self.R[ij] = R_ij
            
            #ahora construimos el error
            m,b = error_multimetro(muestra[ij]['range'])
            c_a = R_ij * m / 100 + b
            c_b = (muestra[ij]['R_max'] - muestra[ij]['R_min'])/np.sqrt(200)
            self.R_error[ij] = c_a + c_b
            
    def error_multimetro(rango):
        if rango == '10k':
            m = 0.1 #porcentaje 
            b = 3 # adicional
            return m, b

    
    # ver como agregar lo de la resistencia