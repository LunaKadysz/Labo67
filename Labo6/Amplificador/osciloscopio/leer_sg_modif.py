# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:38:37 2023

@author: INTI
"""

# Python Version 3.7.0
# This Python example assumes proper reference to the VISA library
# Please refer to application notes and sections of the manual of initial setups
import pyvisa as visa
import time
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd

def main():
    rm = visa.ResourceManager()
    
    # Open Session to Scope with LXI Connection with VISA resource string
    lecroy = rm.open_resource("TCPIP0::LECROY-XPEMBEDD::inst0::INSTR")

    lecroy.write("chdr off")
    
    #channel 1
    vdiv1 = lecroy.query("c1:vdiv?")
    ofst1 = lecroy.query("c1:ofst?")
    
    #channel 2
    vdiv2 = lecroy.query("c2:vdiv?")
    ofst2 = lecroy.query("c2:ofst?")
    
    #variables tiempo
    tdiv = lecroy.query("tdiv?")
    sara = lecroy.query("MSIZ?")
    wvst = lecroy.query("wfsu?")
    print('ch1',vdiv1, ofst1, tdiv, sara,wvst)
    print('ch2',vdiv2, ofst2, tdiv, sara,wvst)
    '''
    sara_unit = {'G':1E9, 'M':1E6,'k':1E3}
    for unit in sara_unit.keys():
        if sara.find(unit) !=-1:
            sara = sara.split(unit)
            sara = float(sara[0])*sara_unit[unit]
            break
        '''
    sara = float(sara)
    #get data ch1
    lecroy.write("c1:wf? dat1")
    recv1 = list(lecroy.read_raw())[16:]
    recv1.pop()
    recv1.pop()
    #get data ch2
    lecroy.write("c2:wf? dat1")
    recv2 = list(lecroy.read_raw())[16:]
    recv2.pop()
    recv2.pop()
    
    
    volt_value1 = []
    volt_value2 = []

    for data in recv1:
        if data > 127:
            data = data -255
        else:
            pass
        volt_value1.append(data)
        
    for data in recv2:
        if data > 127:
            data = data -255
        else:
            pass
        volt_value2.append(data)
        
    
    time_value1 = []
    time_value2 = []
    
    for idx in range(0,len(volt_value1)):
        volt_value1[idx] = volt_value1[idx]/25*float(vdiv1)-float(ofst1)
        time_data = -(float(tdiv)*14/2)+idx*(1/sara)
        time_value1.append(time_data)
        
    for idx in range(0,len(volt_value2)):
        volt_value2[idx] = volt_value2[idx]/25*float(vdiv2)-float(ofst2)
        time_data = -(float(tdiv)*14/2)+idx*(1/sara)
        time_value2.append(time_data)       
        
    plt.figure(figsize=(7,5))
    plt.plot(time_value1,volt_value1,linestyle='none',marker='o',label=u"Y_T")
    plt.plot(time_value2,volt_value2,linestyle='none',marker='o',label=u"Y_T")
    plt.legend()
    plt.grid()
    plt.show()
    
    #freq
    freq = '100khz_2'
    
    
    #save data
    r1=np.asarray(volt_value1)
    r2=np.asarray(volt_value2)
    np.savetxt(f"data/ch1_{freq}.csv",r1)
    np.savetxt(f"data/ch2_{freq}.csv",r2)
    d1 = {'V_div': vdiv1,'offset': ofst1,'T_div': tdiv,'n_meas': sara,'wvst':wvst}
    d2 = {'V_div': vdiv2,'offset': ofst2,'T_div': tdiv,'n_meas': sara,'wvst':wvst}
    np.save(f"data/ch1_{freq}_data.csv", d1)
    np.save(f"data/ch2_{freq}_data.csv", d2)

if __name__=='__main__':
    main()