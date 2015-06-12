import time
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.connect("iot.eclipse.org", 1883, 60)

# Reads the 1-wire bus slave ids into and array
def getSensorIDs():
    ids = []
    with open("/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves") as f:
        for id in f:
            ids.append(id.rstrip())
    return ids

# We assume there is only one device on the 1-wire bus...
device = getSensorIDs()[0]
topic = "RHSummit2015_temp_rpi_DS18B20/" + device
print "publishing to: " + topic
while 1:
    tempfile = open("/sys/bus/w1/devices/" + device + "/w1_slave")
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    temp = float(tempdata[2:]) / 1000
    tempF = temp * 1.8 + 32
    now = time.time()
    json = "{{'sensorid':'{:s}', 'temp':{:.2f}, 'time': {:f}}}".format(device, temp, now)
    print json
    client.publish(topic, json)
    time.sleep(1)
