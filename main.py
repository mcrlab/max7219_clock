import max7219
from machine import Pin, SPI
import time
import machine
from network import WLAN
from time import sleep
from credentials import SSID, PASSWORD
import ntptime

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(33), mosi=Pin(16))
ss = Pin(18, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 4)
display.brightness(1)
    
def connect_to_wifi(ssid, password):
    wlan = WLAN(0)
    wlan.active(True)
    sleep(1.0)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():    
            sleep(1.0)
            pass

    print('Network config:', wlan.ifconfig()) 
    sleep(1.0)

def main():
    connect_to_wifi(SSID, PASSWORD)

    ntptime.settime()

    while True:
        now = time.localtime()
        display.fill(0)
        display.text("{:02d}".format(now[3]),-1,0,1)
        display.text("{:02d}".format(now[4]),17,0,1)
        
        if now[5] % 2 == 0:
            display.rect(15,1,2,2,1)
            display.rect(15,4,2,2,1)
        
        display.show()
        time.sleep(1)

main()

