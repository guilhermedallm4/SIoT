from tinytuya import * 
import json
#from getmac import get_mac_address as gma


ip_mac = []
idDevice = []
ipDevice = []
keyDevice = []
versionDevice = []
d = []


c = Cloud(
        apiRegion="us", 
        apiKey="xq7nmffg4949uacuncmq", 
        apiSecret="eda742de397a4ce5a33218ed24942a6d", 
        apiDeviceID="ebca8c81c4d50747224edf")

devices_ = c.getdevices()
print("Device List: %r" % devices_)


with open("devices.json", "w") as device:     
    json.dump(devices_, device, indent=4)

devices = deviceScan(50)

with open("snapshot.json", 'r') as my_json:
	dados = json.loads(my_json.read())
print(dados)


for i in dados['devices']:
        idDevice.append(i['id'])
        ipDevice.append(i['ip'])
        keyDevice.append(i['key'])
        versionDevice.append(i['ver'])



d = []
for i in range(len(keyDevice)):
        if(ipDevice[i] != '') and (idDevice[i] != '') and (keyDevice[i] != ''):
                d.append(OutletDevice(idDevice[i], ipDevice[i], keyDevice[i]))
                d[i].set_version(3.3)
print(d)

print(d[0].status())

