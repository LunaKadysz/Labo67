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

SetDataSampleRate(SR830,7);
print(GetDataSampleRate(SR830));

SetEndOfBuffer(SR830,0);
print(GetEndOfBuffer(SR830));
#Trigger(SR830);

SetTriggerStartMode(SR830,1);
print(GetTriggerStartMode(SR830));

print('Starting to measure')

Start(SR830);
sleep(1)
Pause(SR830);

#SR830.write('REST') #reset
#data = SR830.query('TRCA? 1,1,4')

def GetDataPoints(ins,buffer,n_points):
	data = ins.query(f'TRCA? {buffer},0,{n_points}')
	return data

print(f'data: {GetDataPoints(SR830,1,5)}')
print(SR830.query('SPTS?'))
#%%
    def SetTriggerSlope(self, value):
        """
        The RSLP command sets the reference trigger when using the
        external reference mode. The parameter i selects sine zero crossing
        (i=0), TTL rising edge (i=1), , or TTL falling edge (i=2). At frequencies
        below 1 Hz, the a TTL reference must be used[1].
        """
        if value not in (0,1,2):
            raise Exception("SetTriggerSlope: parameter value can only be 0(≙sine zero crossing), 1(≙TTL rising edge/Pos edge) or 2(≙TTL falling edge/neg edge)")
        snd = "RSLP%i" % value 
        self.SendString(snd)

    def iToSlope(self, i):
        """
        converts the response returned by GetTriggerSlope to the actual slope
        """
        options = {0 : 'Sine',
           1 : 'Pos edge',
           2 : 'neg edge'
        }
        return options[int(i.strip())]          
    
    def GetTriggerSlope(self):
        """
        The RSLP? command queries the reference trigger when using the
        external reference mode.
        use the method self.iToSlope to convert the response of this method to the actual slope
        """
        resp = self.__GetSomething('RSLP?');
        return resp
        
    def Reset(self):
        """
        Reset the unit to its default configurations[1].
        """
        self.SendString('*RST')
        
    def ResetDataBuffers(self):
        """
        The REST command resets the data buffers. The REST command can
        be sent at any time - any storage in progress, paused or not, will be
        reset. This command will erase the data buffer[1].
        """
        self.SendString('REST')
       
    def GetSelectedOutput(self, which):
        """
        The OUTP? i command reads the value of X, Y, R or θ. The parameter
        i selects X (i=1), Y (i=2), R (i=3) or θ (i=4). Values are returned as ASCII
        floating point numbers with units of Volts or degrees. For example, the
        response might be "-1.01026". This command is a query only command[1].
        """
        if which not in (1,2,3,4):
            raise Exception("GetSelectedOutput: parameter which can only be 1(≙X),2(≙Y),3(≙R) or 4(≙θ)") 
        Value = self.__GetSomething('OUTP?' + str(which))
        if which == 1:
            Type = 'X'
        elif which == 2:
            Type = 'Y'
        elif which == 3:
            Type = 'R'
        elif which == 4:    
            Type = 'θ'
            
        return [float(Value), Type]

    def GetSelectedDisplayValue(self, which):
        """
        The OUTR? i command reads the value of the CH1 or CH2 display.
        The parameter i selects the display (i=1 or 2). Values are returned as
        ASCII floating point numbers with units of the display. For example, the
        response might be "-1.01026". This command is a query only command[1].
        """
        if which not in (1, 2):
            raise Exception("GetSelectedDisplayValue: parameter which can only be 1(≙CH1) or 2(≙CH2)")
        Value =   self.__GetSomething('OUTR?' + str(which)) 
        time.sleep(0.2);
        resp = float(Value)
        if DEBUG:
            print("GetSelectedDisplayValue: " + Value)
        return resp
        
    def __check_snap(self, param):
        """
        internal function used by method SNAP
        ensures that the SNAP-params are correct
        """
        if param not in (1,2,3,4,5,6,7,8,9,10,11):
            raise Exception("SNAP: Parameters can only be 1(≙X), 2(≙Y), 3(≙R), 4(≙θ), 5(≙Aux In 1), 6(≙Aux In 2), 7(≙Aux In 3), 8(≙Aux In 4), 9(≙Reference Frequency), 10(≙CH1 display) or 11(≙CH2 display)") 
        
    def SNAP(self,Param1,Param2,Param3=None,Param4 =None,Param5=None,Param6=None):
        """
        The SNAP? command records the values of either 2, 3, 4, 5 or 6 param-
        eters at a single instant. For example, SNAP? is a way to query values of
        X and Y (or R and θ) which are taken at the same time. This is important
        when the time constant is very short. Using the OUTP? or OUTR? com-
        mands will result in time delays, which may be greater than the time con-
        stant, between reading X and Y (or R and θ).
        The SNAP? command requires at least two parameters and at most six
        parameters. The parameters i, j, k, l, m, n select the parameters below.
        
        i,j,k,l,m,n     parameter
        1               X
        2               Y
        3               R
        4               θ
        5               Aux In 1
        6               Aux In 2
        7               Aux In 3
        8               Aux In 4
        9               Reference Frequency
        10              CH1 display
        11              CH2 display

        The requested values are returned in a single string with the values sep-
        arated by commas and in the order in which they were requested. For
        example, the SNAP?1,2,9,5 will return the values of X, Y, Freq and
        Aux In 1. These values will be returned in a single string such as
        "0.951359,0.0253297,1000.00,1.234".
        The first value is X, the second is Y, the third is f, and the fourth is
        Aux In 1.
        The values of X and Y are recorded at a single instant. The values of R
        and θ are also recorded at a single instant. Thus reading X,Y OR R,θ
        yields a coherent snapshot of the output signal. If X,Y,R and θ are all
        read, then the values of X,Y are recorded approximately 10μs apart from
        R,θ. Thus, the values of X and Y may not yield the exact values of R and
        θ from a single SNAP? query.
        The values of the Aux Inputs may have an uncertainty of up to 32μs. The
        frequency is computed only every other period or 40 ms, whichever is
        longer.
        
        The SNAP? command is a query only command. The SNAP? command
        is used to record various parameters simultaneously, not to transfer data
        quickly[1].
        """
        self.__check_snap(Param1);      
        self.__check_snap(Param2); 
        Cmdstr = 'SNAP?' + ' '+ str(Param1) + ','+ str(Param2);
        if Param3 != None:
            self.__check_snap(Param3); 
            Cmdstr += ','+ str(Param3);
        if Param4 != None:
            self.__check_snap(Param4); 
            Cmdstr += ','+ str(Param4);
        if Param5 != None:
            self.__check_snap(Param5); 
            Cmdstr += ','+ str(Param5);
        if Param6 != None:
            self.__check_snap(Param6); 
            Cmdstr += ','+ str(Param6);

        resp = self.__GetSomething(Cmdstr);
        
        if Param3 is None: # no value, just the command string to query
            Val6 = None; Val5 = None; Val4 = None; Val3 = None 
            [Val1,Val2] = resp.rsplit(',')
        elif Param4 is None: 
            Val6 = None; Val5 =None;  Val4 = None 
            [Val1,Val2,Val3]= resp.rsplit(',')
        elif Param5 is None:
            Val6 = None; Val5 = None; 
            [Val1,Val2,Val3,Val4]= resp.rsplit(',')
        elif Param6 is None:
            Val6 = None 
            [Val1,Val2,Val3,Val4,Val5]= resp.rsplit(',')
        else:
            [Val1,Val2,Val3,Val4,Val5, Val6]= resp.rsplit(',')

        return Val1, Val2, Val3, Val4, Val5, Val6, Param1, Param2, Param3, \
                Param4, Param5, Param6

    def GetAuxValue(self, number):
        """
        The OAUX? command reads the Aux Input values. The parameter i
        selects an Aux Input (1, 2, 3 or 4) and is required. The Aux Input voltages
        are returned as ASCII strings with units of Volts. The resolution is
        1/3 mV. This command is a query only command[1].
        """
        if number not in (1,2,3,4):
            raise Exception("GetAuxValue: parameter number can only be 1(≙Aux Input 1), 2(≙Aux Input 2), 3(≙Aux Input 3) or 4(≙Aux Input 4)") 
        OutAux = self.__GetSomething('OAUX?' + str(number))
        return float(OutAux), number

    def GetOccupiedBuffer(self):
        """
        The SPTS? command queries the number of points stored in the buffer.
        Both displays have the same number of points. If the buffer is reset, then
        0 is returned. Remember, SPTS? returns N where N is the number of
        points - the points are numbered from 0 (oldest) to N-1 (most recent).
        The SPTS? command can be sent at any time, even while storage is in
        progress. This command is a query only command[1].
        """
        n = self.__GetSomething('SPTS?')
        return int(n)