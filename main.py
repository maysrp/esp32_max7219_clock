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
            wlan.connect('wifiname','password')
    def dp(self):
        hspi = SPI(1, baudrate=10000000, polarity=0, phase=0)
        self.display = max7219.Matrix8x8(hspi,Pin(5),4)
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

while 1:
    Clock.show_time()
    time.sleep(1)
    if Clock.m==10:
        Clock.ntp()
