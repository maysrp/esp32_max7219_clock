# esp32_max7219_clock
ESP32 Max7219 Clock

你的ESP32首先要刷好了Micropython固件


按照下图连线：  

esp32     max7219  
5v（或者3v3） vcc  
GND   GND  
G27   DIN  
G26  CS  
G25 CLK  


修改main.py的WiFi名称和密码，上传到你的ESP32上
max7219.py这个库文件也上传到你的esp32上
你的ESP32的时钟就完成了
