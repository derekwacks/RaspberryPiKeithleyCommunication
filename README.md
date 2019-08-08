# RaspberryPiKeithleyCommunication

Notes:
To publish to the mosquitto server: 

`mosquitto_pub -h 160.39.198.70 -t "test/message" -m "import visa import time rm = visa.ResourceManager('@py') address = "ASRL/dev/ttyUSB0::INSTR" inst = rm.open_resource(address) inst.write("*RST") print(inst.query("*IDN?")) inst.write("FORM:DATA ASCII") “ `


Example script: get’s keithley to beep

```
import visa 
import time 
rm = visa.ResourceManager('@py') 
address = "ASRL/dev/ttyUSB0::INSTR"
inst = rm.open_resource(address) 
inst.write("*RST") print(inst.query("*IDN?")) 
inst.write("FORM:DATA ASCII") 
inst.write(“:SYSt:BEEP 100, 3“)
 
inst.close()

```
