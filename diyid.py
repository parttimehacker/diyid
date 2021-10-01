#!/usr/bin/python3
""" Diyhas raspberry pi identification """

# MIT License
#
# Copyright (c) 2019 Dave Wilson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import time
import datetime
import socket
import logging
import logging.config

# imported third party classes

import paho.mqtt.client as mqtt
import psutil

# imported application classes

from pkg_classes.oledcontroller import OLEDController

# standard DIYHA classes

from pkg_classes.testmodel import TestModel
from pkg_classes.topicmodel import TopicModel
from pkg_classes.whocontroller import WhoController
from pkg_classes.configmodel import ConfigModel
from pkg_classes.statusmodel import StatusModel

# Start logging and enable imported classes to log appropriately.

LOGGING_FILE = '/usr/local/diyid/logging.ini'
logging.config.fileConfig( fname=LOGGING_FILE, disable_existing_loggers=False )
LOGGER = logging.getLogger(__name__)
LOGGER.info('Application started')

# get the command line arguments

CONFIG = ConfigModel(LOGGING_FILE)

# Location is used to create the switch topics

TOPIC = TopicModel()  # Location MQTT topic
TOPIC.set(CONFIG.get_location())

# Set up who message handler from MQTT broker and wait for client.

WHO = WhoController(LOGGING_FILE)

# process diy/system/test development messages

TEST = TestModel(LOGGING_FILE)

# Initialize devices

OLED = OLEDController() # Seven segment LED backpack from Adafruit
OLED.clear()


class Host_Information():
    ''' Set up constants and unique server ID stuff '''
    def __init__(self, ):
        ''' server system status monitor thread with MQTT reporting '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #connect to any target website
        sock.connect(('google.com', 0))
        self.host_name = socket.gethostname()+" "
        self.ip_address = sock.getsockname()[0]+" "
        sock.close()


HOST = Host_Information()

def system_message(msg):
    ''' process system messages'''

    if msg.topic == 'diy/system/who':
        if msg.payload == b'ON':
        	WHO.turn_on()
            OLED.clear()
            OLED.set(0, HOST.host_name)
            OLED.set(1, HOST.ip_address)
            OLED.set(2, CONFIG.application)
            OLED.set(3, CONFIG.location)
            OLED.show()
        else:
        	WHO.turn_off()
            OLED.clear()
    elif msg.topic == 'diy/system/fire':
        if msg.payload == b'ON':
            OLED.clear()
            OLED.set(0, HOST.host_name)
            OLED.set(1, "FIRE FIRE FIRE)
			now = datetime.datetime.now()
            OLED.set(2, now.strftime("%Y-%m-%d %H:%M:%S"))
            OLED.set(3, CONFIG.location)
            OLED.show()
        else:
            OLED.clear()
	elif msg.topic == 'diy/system/panic':
        if msg.payload == b'ON':
            OLED.clear()
            OLED.set(0, HOST.host_name)
            OLED.set(1, "PANIC PANIC PANIC)
			now = datetime.datetime.now()
            OLED.set(2, now.strftime("%Y-%m-%d %H:%M:%S"))
            OLED.set(3, CONFIG.location)
            OLED.show()
        else:
            OLED.clear()

# use a dispatch model for the subscriptions
TOPIC_DISPATCH_DICTIONARY = {
    "diy/system/fire":
        {"method":system_message},
    "diy/system/panic":
        {"method":system_message},
    "diy/system/who":
        {"method":system_message},
    }

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rcdata):
    ''' if we lose the connection & reconnect, subscriptions will be renewed '''
    client.subscribe("diy/system/fire", 1)
    client.subscribe("diy/system/panic", 1)
    client.subscribe("diy/system/who", 1)

def on_disconnect(client, userdata, rcdata):
    ''' disconnect message from MQTT broker '''
    client.connected_flag = False
    client.disconnect_flag = True

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    """ dispatch to the appropriate MQTT topic handler """
    TOPIC_DISPATCH_DICTIONARY[msg.topic]["method"](msg)

if __name__ == '__main__':

    # Setup MQTT handlers then wait for timed events or messages

    CLIENT = mqtt.Client()
    CLIENT.on_connect = on_connect
    CLIENT.on_disconnect = on_disconnect
    CLIENT.on_message = on_message

   # initilze the Who client for publishing.

    WHO.set_client(CLIENT)

    # command line argument for the switch mode - motion activated is the default

    CLIENT.connect(CONFIG.get_broker(), 1883, 60)
    CLIENT.loop_start()
    
    # let MQTT stuff initialize

    time.sleep(2) 

    # initialize status monitoring

    STATUS = StatusModel(CLIENT)
    STATUS.start()

    # loop forever checking for interrupts or timed events

    while True:
        time.sleep(10.0)
