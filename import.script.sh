#/usr/bin/bash
#
# import required python libraries

echo "Install Mqtt and psutil"
sudo pip3 install paho-mqtt
sudo pip3 install psutil

echo "Install Adafruit stuff"
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python3 setup.py install
cd ..
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python3 setup.py install
cd ..
