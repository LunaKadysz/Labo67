# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:31:20 2023

@author: DMC
"""

import pyvisa
import csv
import time
import numpy as np

rm = pyvisa.ResourceManager()
print(rm.list_resources())

#%% 

name = 'GPIB0::14::INSTR' #nombre del instrumento
ins = rm.open_resource(name)
print(ins.query("*IDN?"))
#ins.close()

#%% 

#Preparo el aparato 
ins.write('SENSE:FUNCTION:FRESISTANCE')
print(f"MAGNITUD MEDIDA: {ins.query('SENSE:FUNCTION?')}")

ins.write('MEASUREMENT MENU:AC FILTER:SLOW') #NO FUNCIONA

ins.write('SAMPLE:COUNT 1')
print(f"SAMPLE COUNT: {ins.query('SAMPLE:COUNT?')}")

ins.write('TRIGGER:SOURCE BUS')
print(f"TRIGGER: {ins.query('TRIGGER:SOURCE?')}")
#ins.write('MEASUREMENT MENU:RESOLUTION:6 DIGITS')




#%%
#Mido
ins.timeout = 5000
Rs = ins.query_ascii_values('READ?')
print('Comienzo medicion')

"""
#No funciona:
ins.assert_trigger()
ins.wait_for_srq()
print('Medicion completa')
Rs = ins.query_ascii_values("TRACE:DATA?")
"""

#%%
# caluclar promedio
ins.write('CALC:FUNC AVER')

#%%
import pandas as pd
df = pd.DataFrame({'i': [],'j': [], 'R_min':[], 'R_max':[], 'R_avg':[]})

#%% 
#sin trigger porque no me funciona
#20 mediciones es aprox 10s

i = 1
j = 3

#R = f'({i},{j})'

Rs = []
a = time.time()
for n in range(20):
    r = ins.query_ascii_values('MEASURE:FRES?')[0]
    Rs.append(r)
b= time.time()
print(f'tiempo: {b-a}')

df = df.append({'i': i, 'j': j,'R_avg':np.mean(Rs),'R_min':min(Rs),'R_max':max(Rs)},ignore_index=True)


#%%
df.to_csv('data/caja_cuantica.csv', index=False)

