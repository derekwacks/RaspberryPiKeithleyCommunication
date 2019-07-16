"""
Adapted from Keithley User manual to communcate with Raspberry PI using Pyvisa
7.16.19
Derek Wacks 
"""
import visa 
import time 

rm = visa.ResourceManager('@py') 
address = "ASRL/dev/ttyUSB0::INSTR"

inst = rm.open_resource(address) 
inst.write("*RST") print(inst.query("*IDN?")) 
inst.write("FORM:DATA ASCII") 
inst.write(“:SYSt:BEEP 100, 3“)
 
inst.close()

