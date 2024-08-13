A too simple micropython BLE framework inspired by webframeworks. Uses the first word recieved as the route and all the following characters/numbers as parameters. 

Installation:
Copy MicroBLE.py to your micropython device / Create a new file named MicroBLE.py on your device in Thonny and paste its raw content.

From MicroBLE import MicroBLE


Example:
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

@ble.route('hello', request=True) #Use the request=True flag when you want the function to recieve parameters. request comes as a list with strings and ints already converted to int data types. Eg: ['World',123,'thirdparam',4]
def blink(request):
    print("Request:", request)
    return "Hello " + str(request[0])

ble.run()
```



Tested this on a Micropython ESP32 and also WebBle on chrome desktop & android. 
