from tinytuya import * 
import json
from getmac import get_mac_address as gma
import os
import time

#os.system('python -m tinytuya wizard -h')
#time.sleep(5)
#os.system('Y')

ip_mac = []
idDevice = []
ipDevice = []
keyDevice = []
versionDevice = []

c = Cloud(
        apiRegion="us", 
        apiKey="xq7nmffg4949uacuncmq", 
        apiSecret="eda742de397a4ce5a33218ed24942a6d", 
        apiDeviceID="ebca8c81c4d50747224edf")

devices_ = c.getdevices()
print("Device List: %r" % devices_)

devices = deviceScan(50)

with open("snapshot.json", 'r') as my_json:
	dados = json.loads(my_json.read())
print(dados)
counter = 0

for i in dados['devices']:
        idDevice.append(i['id'])
        ipDevice.append(i['ip'])
        keyDevice.append(i['key'])
        versionDevice.append(i['ver'])
        counter = counter + 1

print(keyDevice)
print(ipDevice)
d = []
for i in range(len(keyDevice)):
        if(ipDevice[i] != '') and (idDevice[i] != '') and (keyDevice[i] != ''):
                d.append(OutletDevice(idDevice[i], ipDevice[i], keyDevice[i]))
                d[i].set_version(3.3)
print(d)

print(d[0].status())

