import bluetooth
import time

class MicroBLE():
    def __init__(self, name="MicroBLE", debug=False):
        self.name = name
        self.debug = debug
        self.routes = {}
        self.ble = bluetooth.BLE()
        self.ble.irq(self.ble_irq)
        self.ble.active(True)
        self.register()
        self.advertise()

    def register(self):        
        BLE_NUS = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        BLE_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE)
        BLE_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_NOTIFY)
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def advertise(self):
        name = self.name.encode()
        adv_data = bytearray([0x02, 0x01, 0x06, len(name) + 1, 0x09]) + name
        self.ble.gap_advertise(100, adv_data)
        if self.debug:
            print("Advertising as:", self.name)

    def send(self, data):
        if self.debug:
            print('Response:', data)
        self.ble.gatts_notify(0, self.tx, str(data) + '\n')

    def ble_irq(self, event, data):
        if event == 1:
            if self.debug:
                print("Central Connected")
        elif event == 2:
            if self.debug:
                print('Central disconnected')
            self.advertise()
        elif event == 3:
            request = self.ble.gatts_read(self.rx).decode('UTF-8').strip().split()
            route, *params = request
            route = route.lower()


            
            if self.debug:
                print("Request:", route, params)
            
            if route not in self.routes:
                self.send('Invalid Route')
                return
            
            func, has_params = self.routes[route]
            
            if has_params and not params:
                self.send('Missing Parameters')
                return
            
            response = func(params) if has_params else func()
            
            self.send(response)

    def route(self, route_name, request=False):
        def decorator(f):
            self.routes[route_name.lower()] = (f, request)
            return f
        return decorator
    
    def run(self):
        if self.debug:
            print("Running ",self.name)
        while True:
            time.sleep_ms(100)



