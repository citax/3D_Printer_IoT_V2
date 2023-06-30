import paho.mqtt.client as mqtt

brokerAddress = "12a52b54af3f4191912ad167a7925c0e.s1.eu.hivemq.cloud"
userName = "citak"
passWord = "275452Ahmet"
topic = "my/test/topic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8883)

client.subscribe(topic)

client.loop_forever()
