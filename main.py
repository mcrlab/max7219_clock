import max7219
from machine import Pin, SPI
import time
import machine
from network import WLAN
from time import sleep
from credentials import SSID, PASSWORD
import ntptime
import framebuf

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
    display_time = ""
    
    while True:
        now = time.localtime()
        now_time = "{:02d}{:02d}".format(now[3],now[4])
        if display_time != now_time:
            
            display.fill(0)
            update(now_time)
            display_time = now_time
        else:
            if now[5] % 2 == 0:
                display.rect(15,1,2,2,1)
                display.rect(15,4,2,2,1)
            else:
                display.rect(15,1,2,2,0)
                display.rect(15,4,2,2,0)
            display.show()
        time.sleep(1)
        
def update(new_time):
    f = framebuf.FrameBuffer(bytearray(8),8,8,framebuf.MONO_HLSB)
    for i in range(0,4):
        f.fill(0)
        f.text(new_time[i],0,0)

        if(i < 2):
            delta = -1
        else:
            delta = +1
            
        for y in range(-8,1):
            display.rect((i*8) + delta,0,8,8,0)
            display.blit(f,(i*8)+ delta,y)
            display.show()
            time.sleep(0.0625)
main()

