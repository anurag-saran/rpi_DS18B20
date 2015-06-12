import paho.mqtt.client as mqtt

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

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)
client.loop_forever()
