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

import psutil
import paho.mqtt.client as mqtt
import diyoled128x64

OLED = diyoled128x64.DiyOLED128x64()

logging.config.fileConfig(fname='/home/an/diyid/logging.ini', disable_existing_loggers=False)

# Get the logger specified in the file
LOGGER = logging.getLogger("diyid")

LOGGER.info('Application started')

class MqttTopicConfiguration:
    """ motion_topic to avoid global PEP8 """

    def __init__(self):
        """ create two topics for this application """
        self.setup_topic = "diy/" + socket.gethostname() + "/setup"
        self.location_topic = ""
    def set(self, topic):
        """ the motion topic is passed to the app at startup """
        self.location_topic = topic
    def get_setup(self,):
        """ the motion topic dynamically set """
        return self.setup_topic
    def get_location(self,):
        """ the motion topic dynamically set """
        return self.location_topic

LOCATION_TOPIC = MqttTopicConfiguration()

class Configuration():
    ''' Set up constants and unique server ID stuff '''
    def __init__(self, ):
        ''' server system status monitor thread with MQTT reporting '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #connect to any target website
        sock.connect(('google.com', 0))
        self.host = socket.gethostname()+" "
        self.ip_address = sock.getsockname()[0]+" "
        sock.close()
        self.location = "Default"
        self.mqtt_address = "192.168.1.53"
        self.application = "diysensor"

    def set_application(self, application):
        ''' set the application name '''
        self.application = application

    def set_location(self, location):
        ''' set the application name '''
        self.location = location

CONFIG = Configuration()

def system_message(msg):
    ''' process system messages'''
    if msg.topic == 'diy/system/who':
        if msg.payload == b'ON':
            OLED.set(0, CONFIG.host)
            OLED.set(1, CONFIG.ip_address)
            OLED.set(2, CONFIG.application)
            OLED.set(3, CONFIG.location)
            OLED.show()
        else:
            OLED.clear()
    elif msg.topic == LOCATION_TOPIC.get_setup():
        topic = msg.payload.decode('utf-8')
        LOCATION_TOPIC.set(topic)
        CONFIG.set_location(topic)

# use a dispatch model for the subscriptions
TOPIC_DISPATCH_DICTIONARY = {
    "diy/system/fire":
        {"method":system_message},
    "diy/system/panic":
        {"method":system_message},
    "diy/system/who":
        {"method":system_message},
    LOCATION_TOPIC.get_setup():
        {"method":system_message}
    }

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rcdata):
    ''' if we lose the connection & reconnect, subscriptions will be renewed '''
    client.subscribe("diy/system/fire", 1)
    client.subscribe("diy/system/panic", 1)
    client.subscribe("diy/system/who", 1)
    client.subscribe(LOCATION_TOPIC.get_setup(), 1)

def on_disconnect(client, userdata, rcdata):
    ''' disconnect message from MQTT broker '''
    client.connected_flag = False
    client.disconnect_flag = True

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    """ dispatch to the appropriate MQTT topic handler """
    TOPIC_DISPATCH_DICTIONARY[msg.topic]["method"](msg)

if __name__ == '__main__':

    CLIENT = mqtt.Client()
    CLIENT.on_connect = on_connect
    CLIENT.on_disconnect = on_disconnect
    CLIENT.on_message = on_message
    CLIENT.connect("192.168.1.53", 1883, 60)
    CLIENT.loop_start()

    # give network time to startup - hack?
    time.sleep(1.0)

    # loop forever checking for interrupts or timed events

    while True:
        time.sleep(10.0)
