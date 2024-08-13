A (too) simple micropython BLE app inspired by webframeworks I made for myself. Uses the first word recieved as the route and all the following characters/numbers as parameters. 

Installation:
Copy MicroBLE.py to your micropython device 
or Create a new file named MicroBLE.py on your device in Thonny and paste the raw content.

Use the request=True flag when you want the function to recieve parameters. Request comes as a list with strings and numbers already converted to int data types. 
Eg: ['World',123,'thirdparam',4]

From MicroBLE import MicroBLE


Example Useage:
```
#main.py
from machine import Pin
from MicroBLE import MicroBLE

led = Pin(2, Pin.OUT)

ble = MicroBLE(name='MicroBLE', debug=True)

@ble.route('toggle')
def toggle():
    led.value(not led.value())
    return "LED ON" if led.value() else "LED OFF"

@ble.route('status')
def status():
    return "LED ON" if led.value() else "LED OFF"

@ble.route('hello', request=True) 
def blink(request):
    print("Request:", request) #['World',123,'thirdparam',4]
    return "Hello " + str(request[0]) 

ble.run()
```



Tested this on a Micropython ESP32, Bluetooth Serial Monitor on android and also using WebBle on chrome desktop & android. 

Uses a single service and characteristics, that could be a limitation for your use case. Piggybacked on code shared by others and also got some help from chatgpt.
