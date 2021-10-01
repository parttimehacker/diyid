# diyid
Do It Yourself Raspberry Pi server identification application in Python3 using common OLED display. Used to identify a Pi server with the following information. 
- Host name
- IP address
- Main application name
- Location topic string

## Requires:
```
import time
import datetime
import socket
import logging
import logging.config
import psutil
import paho.mqtt.client as mqtt
import diyoled128x64e
```

## Install:
```
sudo pip3 install paho-mqtt
sudo pip3 install psutil
```

## Useful utilities:
```
sudo pip3 install pylint
sudo apt -y install screen
```

## Setting up systemctl service
It is a good idea to run diyis.py as a system service at boot time. The setup bash script will move the systemctl files to
the /lib/systemd/system folder; enable the service and create three useful aliases: start, stop and status.
- Edit the diystatus.service file and enter your user directory 
- Enter the following commands to install the service
```
chmod +x *.sh
./setup.systemctl.sh diyid
```
- Reboot is recommended

