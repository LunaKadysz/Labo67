# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 10:55:13 2023

@author: DMC
"""
import visa
import pyvisa
from time import sleep
import numpy as np
import math
import os
import matplotlib.pyplot as plt
plt.rc('axes', axisbelow=True) # This is for plotting data in front of the grid.
plt.rcParams.update({'font.size': 8}) # Changes the default font size for the plots.
import datetime

path_abs = r'C:\Users\Usuario\Documents\luna_kadysz\Labo67\Labo6\Amplificador'
os.chdir(path_abs)
#os.getcwd()

def time_constant_number(t):
	t_constant = [10e-6, 30e-6, 100e-6, 300e-6, 1e-3, 3e-3, 10e-3, 30e-3, 100e-3, 300e-3, 1, 3, 10, 30, 100, 300, 1e3, 3e3, 10e3, 30e3]
	if t < t_constant[0]:
		return 0
	for k in range(0, len(t_constant)-1):
		if t >= t_constant[k] and t < t_constant[k+1]:
			return k

rm = pyvisa.ResourceManager()
print("rm.list_resources() returns this --> ", rm.list_resources())
SR830 = rm.open_resource('GPIB0::8::INSTR')

#%%

SR830.query('*IDN?') # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
SR830.query('*IDN?') # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
SR830.query('*IDN?') # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
SR830.query('*IDN?') # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
print('\nThe instrument says this --> ', SR830.query('*IDN?'))

#%%
# MEASURMENT PARAMETERS ------------------------------------
START_FREQUENCY = float(input("Start frequency (Hz)? "))
END_FREQUENCY = float(input("Final frequency (Hz)? "))
N_POINTS = int(input("Number of points? "))
RMS_VOLTAGE = float(input("Excitation voltage (Vrms)? ")) # Excitation voltage.
TIME_FACTOR = 300 # Determines the "time constant" of the lock-in according to "time constant = TIME_FACTOR*frequency". A value of 300 should be enough. Higher values will result in more stable measurments but longer times.
STABILIZATION_TIME_FACTOR = 8 # Determines the delay between the moment in which the frequency is changed and the moment in which the measurment is taken according to "delay = STABILIZATION_TIME_FACTOR*time constant". A value of 8 should be enough. Greater values will result un more realistic values but will take more time.
# ----------------------------------------------------------

#%%


def SetDataSampleRate(ins, rate = 4):
	"""
        The SRAT i command sets the data sample rate. The parame-
        ter i selects the sample rate listed below.
        i   quantity    i   quantity
        0   62.5 mHz    8   16 Hz
        1   125 mHz     9   32 Hz
        2   250 mHz    10   64 Hz
        3   500 mHz    11   128 Hz
        4   1 Hz       12   256 Hz
        5   2 Hz       13   512 Hz
        6   4 Hz       14   Trigger
        7   8 Hz
        [1]
	"""
	ins.write(f'SRAT {rate}')


def GetDataSampleRate(ins, rate = None):
	"""
        The SRAT? command queries the data sample rate[1].
	"""
	Rate = ins.query('SRAT?')
	return int(Rate)        


def SetEndOfBuffer(ins, kind =None):
	"""
        The SEND i command sets the end of buffer mode. The param-
        eter i selects 1 Shot (i=0) or Loop (i=1). If Loop mode is used, make sure
        to pause data storage before reading the data to avoid confusion about
        which point is the most recent[1].
	"""
	if kind not in (0,1):
		raise Exception("SetEndOfBuffer: parameter kind can only be 0(≙Shot) or 1(≙Loop)")
	ins.write(f'SEND {kind}')
        
def GetEndOfBuffer(ins, kind = None):
	"""
        The SEND? command queries the end of buffer mode[1].
	"""
	Kind = ins.query('SEND?')
	return Kind

def Trigger(ins):    
	"""
        The TRIG command is the software trigger command. This command
        has the same effect as a trigger at the rear panel trigger input[1].
        """
	ins.query('TRIG')


        
def SetTriggerStartMode(ins, kind):
	"""
        The TSTR i command sets the trigger start mode. The parameter 
        i=1 selects trigger starts the scan and i=0 turns the trigger start feature off.
        """
	if kind not in (0,1):
		raise Exception("SetTriggerStartMode: parameter kind can only be 0(≙trigger starts the scan) or 1(≙turns the trigger start feature off)")
	ins.write(f'TSTR {kind}')

def GetTriggerStartMode(ins):
	"""
        The TSTR? command queries the trigger start mode[1].
	"""
	Kind = ins.query('TSTR?')
	return int(Kind)

def Start(ins):
	"""
	The STRT command starts or resumes data storage. STRT is ignored if 
	storage is already in progress[1].
	
        The STRT command starts or resumes data storage. STRT is ignored if
        storage is already in progress[1].
        """
	ins.write('STRT')

def Pause(ins): 
	"""
        The PAUS command pauses data storage. If storage is already paused
        or reset then this command is ignored[1].
	"""
	ins.write('PAUS')

def ResetDataBuffers(ins):
	"""
        The REST command resets the data buffers. The REST command can
        be sent at any time - any storage in progress, paused or not, will be
        reset. This command will erase the data buffer[1].
        """
	ins.write('REST')
#%%

#reset before measuring
SR830.write('REST')


#reference signal
SR830.write('FMOD 1') #internal reference mode
SR830.write('FREQ 13.1') # internal reference frequency 
SR830.write('RSLP 1') # type of signal internal reference: TTL rising edge
print(SR830.query('RSLP?'))

#sample rate
sr = 13 # 512Hz
SetDataSampleRate(SR830,sr);
print(GetDataSampleRate(SR830));

SetEndOfBuffer(SR830,0);
print(GetEndOfBuffer(SR830));
#Trigger(SR830);

SetTriggerStartMode(SR830,1);
print(GetTriggerStartMode(SR830));


print('Starting to measure')

Start(SR830);
sleep(0.1)
Pause(SR830);

#SR830.write('REST') #reset
#data = SR830.query('TRCA? 1,1,4')

def GetDataPoints(ins,buffer,n_points):
	data = ins.query(f'TRCA? {buffer},0,{n_points}')
	return data


buffer_points = SR830.query('SPTS?') #number of points stored in the buffer

data = GetDataPoints(SR830,1,buffer_points)
time = np.linspace(0,len(buffer_points)/512,buffer_points)
time = np.arange(0,len(buffer_points)/512,1/512)

plt.plot(time,data)





#%%
