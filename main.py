import time
import ntptime
import network
import max7219
import urequests
from machine import Pin,SPI,RTC
class clock:
    def __init__(self):
        self.id="1369152" #你的Bilibil的ID
        self.wifi="pangxh" #你的WiFi名，只支持2.4GHZ的wifi
        self.password="a12345678" #你的WiFi密码
        self.ntp()
        self.dp()
        self.se=0
        self.rtc=RTC()
        self.fans()
    def net(self):
        wlan = network.WLAN(network.STA_IF) 
        wlan.active(True) 
        if not wlan.isconnected(): 
            wlan.connect(self.wifi,self.password) 
    def dp(self):
        spi = SPI(baudrate=100000, polarity=1, phase=0, mosi=Pin(27),sck=Pin(25), miso=Pin(33))
        self.display = max7219.Matrix8x8(spi,Pin(26),4)
    def ntp(self):
        self.net()
        time.sleep(5)
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
    def fans(self):
        url="http://api.bilibili.com/x/relation/stat?vmid="+str(self.id)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE' }
        re=urequests.get(url,headers=headers)
        my=re.json()
        if my['code']==0:
            self.fans_count= my['data']['follower']
        else:
            self.fans_count=False
    def backfans(self):
        if type(self.fans_count).__name__=='int':
            if self.fans_count<10000:
                return str(self.fans_count)
            elif self.fans_count<1000000:
                ka=self.fans_count//1000
                return str(ka)+'K'
            else:
                ka=self.fans_count//1000000
                return str(ka)+'M'
        else:
            return 'None'
    def show_myfans(self):
        for i in range(9):
            self.display.fill(0)
            self.display.text(self.backfans(),i*4,0,1)
            self.display.show()
            time.sleep(0.2)


Clock=clock()

oldM=0
while 1:
    Clock.show_time()
    time.sleep(1)
    Clock.show_myfans()
    if Clock.m!=oldM:
        Clock.ntp()
        oldM=Clock.m
        Clock.fans()
