# Raspberry Pi & Keithley 2401 Sourcemeter Communication using an MQTT server

## Overall Scheme: 
* Host an MQTT server, using a Raspberry Pi as a topic broker
* Load a .py control script on the Rpi
* Start the Rpi as a subscriber to an MQTT topic of your choice
* edit the MQTT launcher conf file, connecting a message/topic pair to the respective command (for example, connecting `user/bin/python` & `~/home/Documents/myKeithleyControl.py` to your friendly neighborhood `test/message` topic thread with the trigger name `myControl`)
* Run the Keithley control script remotely by publishing an appropriate message payload on the MQTT topic, and having the Keithley connected to the Rpi using a USB-RS232 UART adapter
 
I know what you're thinking. _Why board a plane to travel to the corner deli?_ For lack of a better excuse, because I felt like it and sometimes I prefer the coffee & pancakes in Jet Blue's T5 over my local delicatessen anyways. WebREPL works just fine aswell, and there's a slick way to set up nodeforwader (https://github.com/dansteingart/nodeforwarder) with a serial connection and house all the on-goings on your own machine (described bellow). Maybe that's what I set out to do in the first place, or maybe a state trooper caught me doing 86 in a 65 last weekend after I slowed down from more-than-a-few-mph-faster, or maybe both. Who's to say.

Next I'm trying to finagle running the Keithley control lines one-by-one _as_ the payload, which would make all of this actually useful.


#### The nitty-gritty (notes)
* install the mosquitto MQTT broker with `sudo apt install mosquitto mosquitto-clients`

* enable with `sudo systemctl enable mosquitto`

* install the MQTT client (on your other machine) with `sudo apt install mosquitto-clients`

To publish to the mosquitto server: 

`mosquitto_pub -h IP_or_hostname_or_localhost -t "test/message" -m "payload_or_name_like_myControl_here"`

Subscribe remotely:

`mosquitto_sub -h raspberryPiIP  -t "test/message"` 
(https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi)

* install the Mqtt-launcher (included)
* run  mqtt-launcher.py before publishing a payload locally or remotely

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
```
"test/message"      :   {'example_payload'            :   ["usr/bin/python", 'home/pi/Documents/myControl.py'] }
```

### Credits:
Thanks to JP Mens for a swanky mqtt-launcher https://github.com/jpmens/mqtt-launcher

And Eclipse for an MQTT broker https://github.com/eclipse/mosquitto

__________________________________________________________________

# Raspberry Pi & Keithley 2401 Sourcemeter Communication using nodeforwarder

## Overall Scheme: 

From a laptop or Rpi...
* plug in Keithley & check path (ex: /dev/ttyUSB0 )
* run nodefowarder with `(sudo) node nodefowarder.js 9000 /dev/ttyUSB0 9600 10000` 
where 9000 is the port number, /dev/ttyUSB0 is the path, 9600 is the baud rate (set in Keithley's settings), and 10000 is the buffer (10k gives ample time). 
* go to localhost:9000 or IP address
* send `FORM:DATA:ASCII` to format Keithley
* test with `:SYS:BEEP 100,3`

#### The nitty-gritty (notes)
With the keithley set to RS232 mode, controls should flow through 




