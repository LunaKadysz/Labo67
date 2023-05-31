# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:39:34 2023

@author: DMC
"""
import pyvisa



rm = pyvisa.ResourceManager()
print(rm.list_resources())


#%%


keithley = rm.open_resource(rm.list_resources()[0])
keithley.write("rst; status:preset; cls")


#%%

interval_in_ms = 500
number_of_readings = 5
#keithley.write('status:measurement:enable 512; *sre 1')

keithley.write(f'sample:count {number_of_readings}')
keithley.write('trigger:source bus')
keithley.write(f'trigger:delay {(interval_in_ms / 1000.0)}')
keithley.write(f'trace:points {number_of_readings}')
keithley.write('trace:feed sense1; feed:control next')

#%%

keithley.write("initiate")
keithley.assert_trigger()
keithley.wait_for_srq()