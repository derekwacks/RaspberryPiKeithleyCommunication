# Raspberry Pi & Keithley Communication using an MQTT server

## Overall Scheme: 
* Host an MQTT server, using a Raspberry Pi as a topic broker
* Load a .py control script on the Rpi
* Start the Rpi as a subscriber to an MQTT topic of your choice
* edit the MQTT launcher conf file, connecting a message/topic pair to the respective a command (for example: `user/bin/python` & `~/home/Documents/myKeithleyControl.py`)
* Run the Keithley control script remotely by publishing an appropriate payload & message on the MQTT topic 

You can even run your Keithley control lines one-by-one _as_ the payload 
 
I know what you're thinking. Why'd we board a plane to travel to the corner deli? For lack of a better excuse, because I felt like it and sometimes I prefer the coffee & pancakes in JB's Terminal 5 over my local delicatessen anyways. 


Notes:
To publish to the mosquitto server: 

`mosquitto_pub -h raspberrypi_or_IP -t "test/message" -m "name_set_in_mqtt_conf_file"`


Subscribe remotely:
`mosquitto_sub -h myIP  -t "test/message"` (https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi)


### Example script: 
Gets the Keithley to beep as a test 

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

### Credits:
Thanks to JP Mens for a swanky mqtt-launcher https://github.com/jpmens/mqtt-launcher

And Eclipse for an MQTT broker https://github.com/eclipse/mosquitto
