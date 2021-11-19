import paho.mqtt.client as mqtt
import os
import hashlib
import subprocess
import clipboard

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

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

path = input('Nome da pasta: ')
ident = input('Destinatário: ')

print('Loading...')        
sub = subprocess.Popen("ipfs add -r {}".format(path) , shell=True, stdout=subprocess.PIPE)
subprocess_return = sub.stdout.read()
print()

# Decodificação da saída, chega em utf-8
x = subprocess_return.decode('utf-8')

# Divisão de cada uma das linhas geradas pela saída do CMD para organização
linhas = x.splitlines()
nlinhas = len(linhas)
# print()
print(x)

# Separação da última linha, possui o hash do diretório inteiro (mais importante)
ultima_linha = linhas[nlinhas-1]

print(ultima_linha)
hs = ultima_linha[len('added '):len('added QmR8sZ9axGzHq1gVzgs2o7caht2Hqinj26fezwV5pKkGdj')]
clipboard.copy(hs)

mqttc.publish(ident,hs,0)


# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
