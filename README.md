# Raspberry Pi & Keithley 2401 Sourcemeter Communication using an MQTT server

## Overall Scheme: 
* Host an MQTT server, using a Raspberry Pi as a topic broker
* Load a .py control script on the Rpi
* Start the Rpi as a subscriber to an MQTT topic of your choice
* edit the MQTT launcher conf file, connecting a message/topic pair to the respective command (for example, connecting `user/bin/python` & `~/home/Documents/myKeithleyControl.py` to your friendly neighborhood `test/message` topic thread with the trigger name `myControl`)
* Run the Keithley control script remotely by publishing an appropriate message payload on the MQTT topic, and having the Keithley connected to the Rpi using a USB-RS232 UART adapter

You can even run your Keithley control lines one-by-one _as_ the payload 
 
I know what you're thinking. Why board a plane to travel to the corner deli? For lack of a better excuse, because I felt like it and sometimes I prefer the coffee & pancakes in Jet Blue's T5 over my local delicatessen anyways. 
#### The nitty-gritty (notes)
install the mosquitto MQTT broker with `sudo apt install mosquitto mosquitto-clients`

enable with `sudo systemctl enable mosquitto`

install the MQTT client (on your other machine) with `sudo apt install mosquitto-clients`

To publish to the mosquitto server: 

`mosquitto_pub -h IP_or_hostname_or_localhost -t "test/message" -m "payload_or_name_like_myControl_here"`

Subscribe remotely:

`mosquitto_sub -h raspberryPiIP  -t "test/message"` 
(https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi)


### Example script: 
Gets the Keithley to beep as a test 

```
import visa 
import time 
rm = visa.ResourceManager('@py') 
address = "ASRL/dev/ttyUSB0::INSTR" # Ensure this is the correct path
inst = rm.open_resource(address) 
inst.write("*RST") print(inst.query("*IDN?")) 
inst.write("FORM:DATA ASCII") # This is crucial, otherwise your commands are gibberish 
inst.write(“:SYSt:BEEP 100, 3“)
inst.close()

```
Add this to the launcher.conf file
```"test/message"      :   {'example_payload'            :   ["usr/bin/python", 'home/pi/Documents/myControl.py'] }
```

### Credits:
Thanks to JP Mens for a swanky mqtt-launcher https://github.com/jpmens/mqtt-launcher

And Eclipse for an MQTT broker https://github.com/eclipse/mosquitto
