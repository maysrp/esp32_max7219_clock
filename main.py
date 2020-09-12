import time
import ntptime
import network
import max7219
from machine import Pin,SPI,RTC
class clock:
    def __init__(self):
        self.ntp()
        self.dp()
        self.se=0
        self.rtc=RTC()
    def net(self):
        wlan = network.WLAN(network.STA_IF) 
        wlan.active(True) 
        if not wlan.isconnected(): 
            wlan.connect('pangxh','a12345678') #第一个为你的wifi名称，后一个为wifi密码，只支持2.4GHZ的wifi
    def dp(self):
        spi = SPI(baudrate=100000, polarity=1, phase=0, mosi=Pin(27),sck=Pin(25), miso=Pin(33))
        self.display = max7219.Matrix8x8(spi,Pin(26),4)
    def ntp(self):
        self.net()
        ntptime.host="ntp1.aliyun.com"
        ntptime.NTP_DELTA = 3155644800
        try:
            ntptime.settime()
        except Exception as e:
            pass
    def show_time(self):
        date=self.rtc.datetime()
        self.m=date[5]
        self.h=date[4]
        self.display.fill(0)
        self.display.text(str(self.h) if len(str(self.h))==2 else ' '+str(self.h) ,0,0,1)
        self.display.pixel(16,2,self.se)        
        self.display.pixel(16,4,self.se)        
        self.display.text(str(self.m) if len(str(self.m))==2 else '0'+str(self.m) ,17,0,1)
        self.se=0 if self.se==1 else 1
        self.display.show()
Clock=clock()

oldM=0
while 1:
    Clock.show_time()
    time.sleep(1)
    if Clock.m!=oldM:
        Clock.ntp()
        oldM=Clock.m
