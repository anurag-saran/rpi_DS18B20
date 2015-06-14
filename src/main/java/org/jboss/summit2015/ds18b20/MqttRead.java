package org.jboss.summit2015.ds18b20;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.util.List;

/**
 * Simple MQTT client that subscribes to the temperature sensor topic
 */
public class MqttRead implements MqttCallback {
    private volatile int receiveCount = 0;

    @Override
    public void connectionLost(Throwable throwable) {
        System.out.printf("connectionLost\n");
        throwable.printStackTrace();
    }

    @Override
    public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
        System.out.printf("messageArrived, topic=%s, msg=%s\n", topic, mqttMessage.toString());
        receiveCount ++;
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

    }

    public void run(int count, String id) throws Exception {
        // Just grab first sensor
        String topic = "RHSummit2015_temp_rpi_DS18B20/"+id;

        // TODO: if your running multiple clients you need to make this unique, "RecvTemperatureMQTT#N-" + id;
        // where #N = #1, #2, #3, ...
        String clientID = "RecvTemperatureMQTT-" + id;
        MqttClient client = new MqttClient("tcp://iot.eclipse.org:1883", clientID, new MemoryPersistence());
        client.connect();
        client.subscribe(topic);
        client.setCallback(this);
        System.out.printf("Connected to: tcp://iot.eclipse.org:1883, reading %d messages\n", count);
        while(receiveCount < count) {
            Thread.sleep(1000);
        }
        client.disconnect();
        System.exit(0);
    }
    public static void main(String[] args) throws Exception {
        int count = 1;
        String deviceID;
        if(args.length > 0)
            count = Integer.parseInt(args[0]);
        if(args.length == 2) {
            deviceID = args[1];
        } else {
            List<String> ids = OneWireSensor.getSensorIDs();
            deviceID = ids.get(0);
        }

        MqttRead reader = new MqttRead();
        reader.run(count, deviceID);
    }
}
