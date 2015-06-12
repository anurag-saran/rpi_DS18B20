import time

# Reads the 1-wire bus slave ids into and array
def getSensorIDs():
	ids = []
	with open("/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves") as f:
		for id in f:
			ids.append(id.rstrip())
	return ids


# We assume there is only one device on the 1-wire bus...
device = getSensorIDs()[0]
print "Getting temperature of: "+device
while 1:
	tempfile = open("/sys/bus/w1/devices/"+device+"/w1_slave")
	thetext = tempfile.read()
	tempfile.close()
	tempdata = thetext.split("\n")[1].split(" ")[9]
	temp = float(tempdata[2:])
	temp = temp / 1000
	tempF = temp*1.8 + 32
	print "{:.2f}C or {:.2f}F".format(temp, tempF)
	time.sleep(1)

