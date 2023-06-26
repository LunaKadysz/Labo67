# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:38:21 2023

@author: DMC
"""

# Execute this script using --> exec(open('SR830.py').read())

print("\n"*100) # Just clear the screen.
print("Thanks for using the SR830 Frequency Response program.\nStarting the GPIB comunication, please wait...")

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
		
# MEASURMENT PARAMETERS ------------------------------------
START_FREQUENCY = float(input("Start frequency (Hz)? "))
END_FREQUENCY = float(input("Final frequency (Hz)? "))
N_POINTS = int(input("Number of points? "))
RMS_VOLTAGE = float(input("Excitation voltage (Vrms)? ")) # Excitation voltage.
TIME_FACTOR = 300 # Determines the "time constant" of the lock-in according to "time constant = TIME_FACTOR*frequency". A value of 300 should be enough. Higher values will result in more stable measurments but longer times.
STABILIZATION_TIME_FACTOR = 8 # Determines the delay between the moment in which the frequency is changed and the moment in which the measurment is taken according to "delay = STABILIZATION_TIME_FACTOR*time constant". A value of 8 should be enough. Greater values will result un more realistic values but will take more time.
# ----------------------------------------------------------

#%%

if RMS_VOLTAGE > 5 or RMS_VOLTAGE < 0.004:
	print("ERROR: Invalid excitation voltage. The allowed range is between 0.004 and 5 volts.")
	exit()


SR830.write("OUTX1") # Set the SR830 output response to GPIB port instead of RS232.
SR830.write("*RST") # Initialize the lock-in.
# Reference and phase config -----------------
SR830.write("FMOD 1") # Set (Query) the Reference Source to External (0) or Internal (1).
SR830.write("SLVL " + str(RMS_VOLTAGE)) # Set (Query) the Sine Output Amplitude to x Vrms. 0.004 ≤ x ≤ 5.000.
# Input and filter configuration -------------
SR830.write("ISRC 0") # Set (Query) the Input Configuration to A (0), A-B (1) , I (1 MΩ) (2) or I (100 MΩ) (3).
SR830.write("IGND 0") # Set (Query) the Input Shield Grounding to Float (0) or Ground (1).
SR830.write("ICPL 1") # Set (Query) the Input Coupling to AC (0) or DC (1).
# Gain and time constant ---------------------
SR830.write("SENS 23") # Set (Query) the Sensitivity to 2 nV (0) through 1 V (26) rms full scale.
SR830.write("RMOD 1") # Set (Query) the Dynamic Reserve Mode to HighReserve (0), Normal (1), or Low Noise (2).
SR830.write("OFLT 12") # Set (Query) the Time Constant to 10 μs (0) through 30 ks (19).
SR830.write("OFSL 1") # Set (Query) the Low Pass Filter Slope to 6 (0), 12 (1), 18 (2) or 24 (3) dB/oct.
SR830.write("SYNC 1") # Set (Query) the Synchronous Filter to Off (0) or On below 200 Hz (1).
# Display and output -------------------------
#SR830.write("DDEF 1, 1, 0") # Set (Query) the CH1 or CH2 (i=1,2) display to XY, Rθ, XnYn, Aux 1,3 or Aux 2,4 (j=0..4) and ratio the display to None, Aux1,3 or Aux 2,4 (k=0,1,2).
#SR830.write("DDEF 2, 1, 0") # Set (Query) the CH1 or CH2 (i=1,2) display to XY, Rθ, XnYn, Aux 1,3 or Aux 2,4 (j=0..4) and ratio the display to None, Aux1,3 or Aux 2,4 (k=0,1,2).
SR830.write("DDEF 1, 0, 0") # Set (Query) the CH1 or CH2 (i=1,2) display to XY, Rθ, XnYn, Aux 1,3 or Aux 2,4 (j=0..4) and ratio the display to None, Aux1,3 or Aux 2,4 (k=0,1,2).
SR830.write("DDEF 2, 0, 0") # Set (Query) the CH1 or CH2 (i=1,2) display to XY, Rθ, XnYn, Aux 1,3 or Aux 2,4 (j=0..4) and ratio the display to None, Aux1,3 or Aux 2,4 (k=0,1,2).
SR830.write("FPOP 1, 0") # Set (Query) the CH1 (i=1) or CH2 (i=2) Output Source to X or Y (j=1) or Display (j=0).
SR830.write("FPOP 2, 0") # Set (Query) the CH1 (i=1) or CH2 (i=2) Output Source to X or Y (j=1) or Display (j=0).

SR830.write("FREQ" + str(START_FREQUENCY)) # Set the frequency.
#SR830.write("AGAN") # Auto Gain function. Same as pressing the [AUTO GAIN] key.
#input("The instrument should be performing an automatic sensivity adjustment, and should make a noise signal when it is done. Press enter when it has finished...") # This is to ensure that the previous command has finished.

print("Measuring, please wait...")
frequency = np.array([]) # Create an empty array.
voltage_R = np.array([]) # Create an empty array.
phase = np.array([]) # Create an empty array.
voltage_X = np.array([]) # Create an empty array.
voltage_Y = np.array([]) # Create an empty array.

for k in range(1, N_POINTS + 1):
	frequency = np.append(frequency, 10**( (k-1)*(math.log10(END_FREQUENCY) - math.log10(START_FREQUENCY))/(N_POINTS-1) + math.log10(START_FREQUENCY) ) ) # Logarithmically spaced frequencies.
	SR830.write("FREQ" + str(frequency[-1])) # Set the frequency just calculated.
	SR830.write("OFLT " + str(time_constant_number(TIME_FACTOR/frequency[-1]))) # Set (Query) the Time Constant to 10 μs (0) through 30 ks (19).
	#SR830.write("AGAN")# Auto Gain function. Same as pressing the [AUTO GAIN] key.
	sleep(TIME_FACTOR/frequency[-1]*STABILIZATION_TIME_FACTOR + 5)
	SR830.query("OUTP? 1") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	SR830.query("OUTP? 1") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	SR830.query("OUTP? 1") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	SR830.query("OUTP? 1") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	voltage_X = np.append(voltage_X, float(SR830.query("OUTP? 1")))
	SR830.query("OUTP? 2") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	SR830.query("OUTP? 2") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	SR830.query("OUTP? 2") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	SR830.query("OUTP? 2") # If I don't query at least four times, it may return crap from some buffer (which I don't know how to clear).
	voltage_Y = np.append(voltage_Y, float(SR830.query("OUTP? 2")))
    
	# Nice plot ---------------------------------------------------
	X_AXIS_LABEL = 'Frequency (Hz)'
	Y_AXIS_LABEL = 'Voltage (V)'
	COLORS = ['#000000', '#ff0000', '#0000ff', '#00aa00', '#ff7700', '#008888', '#880088']
	MARKERS = ['.', '', '', '', '', '', '']
	LINESTYLES = ['-', '-', '-', '-', '-', '-', '-']

	FIG_WIDTH = 130e-3 # Figures' width in meters (size of the chart+axis_ticks, not counting legend, title, etc.).
	FIG_RATIO = [1, 0.5] # XY ratio of figures.

	x = [] # Initialize list of "numpy" arrays containing data to be plotted.
	y = [] # Initialize list of "numpy" arrays containing data to be plotted.
	x.append(frequency)
	y.append(np.sqrt((voltage_X)**2 + (voltage_Y)**2))
	# FIGURE ----------------------------------------------	
	fig = plt.figure(num=1, figsize=(FIG_WIDTH*FIG_RATIO[0]/25.4e-3, FIG_WIDTH*FIG_RATIO[1]/25.4e-3))
	ax = fig.add_subplot(111)
	# Plotting the elements -------------------------------
	lines = [] # Creates the empty lines list.
	for k in range(0,len(y)):
		lines.append(ax.plot(x[k], y[k])[0])
		lines[k].set_color(COLORS[k])
		lines[k].set_linewidth(1)
		lines[k].set_linestyle(LINESTYLES[k])
		lines[k].set_marker(MARKERS[k])
		#~ lines[k].set_markersize(3)
	#Axes & tick configuration ------------------------------
	plt.xlabel(X_AXIS_LABEL)
	plt.ylabel(Y_AXIS_LABEL)
	# ax.ticklabel_format(style='sci', axis='x', scilimits=(-2,2)) # Scientific notation for ranges grater than 10^-2 and 10^2.
	# ax.ticklabel_format(style='sci', axis='y', scilimits=(-2,2)) # Scientific notation for ranges grater than 10^-2 and 10^2.
	ax.set_xscale('log') # Logarithmic "x" scale.
	#~ ax.set_yscale('log') # Logarithmic "y" scale.
	ax.minorticks_on() # Enables minor ticks without text, only the ticks.
	# Window configuration ---------------------------------
	ax.autoscale(tight=True)
	factor = 0.1 # Zoom out from "tigth" a factor of 0.1
	xlim = ax.get_xlim()
	ax.set_xlim((xlim[0] + xlim[1])/2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor))
	ylim = ax.get_ylim()
	ax.set_ylim((ylim[0] + ylim[1])/2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor))
	# Grid configuration -----------------------------------
	ax.grid(b=True, which='major', color='#aaaaaa', linestyle='-', linewidth=0.5)
	ax.grid(b=True, which='minor', color='#dddddd', linestyle='-', linewidth=0.25)

	plt.draw()
	plt.pause(0.1)
rm.close()

print("Measurment finished. Close the plot window to continue.")

file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
plt.savefig('data/'+file_name+'_int.pdf', bbox_inches='tight')
header_str = 'frequency (Hz)	Voltage_X (V) 	Voltage_Y (V)'
np.savetxt('data/'+file_name+'.txt', np.transpose([frequency, voltage_X, voltage_Y]), fmt='%1.7e', delimiter='\t', header=header_str, newline='\n', comments='# ')

plt.show()

print("The plot and the CSV data have been saved to files " + file_name + ".pdf and " + file_name + ".txt respectively.")
print("Thanks for using the program, hope to see you back soon, bye!\n\n\n\n")




  





