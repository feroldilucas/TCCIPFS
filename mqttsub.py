import paho.mqtt.client as mqtt
import os
import hashlib
import subprocess
import clipboard
from win10toast import ToastNotifier

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
    hs = msg.payload.decode("utf-8")
    print(hs)
    clipboard.copy(hs)

    toaster = ToastNotifier()
    toaster.show_toast('IPFS', 'Arquivo recebido\n{} copiado para a área de transferência'.format(hs))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.username_pw_set("zucuzzak", "I5HWGWWppSLX")
mqttc.connect("m15.cloudmqtt.com", 10420, 60)

# Start subscribe, with QoS level 0
mqttc.subscribe('hash', 0)
mqttc.subscribe('Pedro', 0)
mqttc.subscribe('Yara', 0)
mqttc.subscribe('Lucas', 0)
mqttc.subscribe('Guilherme', 0)

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
