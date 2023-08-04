import cv2
import paho.mqtt.client as mqtt
import time
import numpy as np
import base64

brokerAddress = "12a52b54af3f4191912ad167a7925c0e.s1.eu.hivemq.cloud"
userName = "citak"
passWord = "275452Ahmet"
topic = "my/test/topic"
data = "Hello from Away Machine"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

def on_message(client, userdata, msg):
    global frame
    img = base64.b64decode(msg.payload)
    npimg = np.frombuffer(img, dtype=np.uint8)
    frame = cv2.imdecode(npimg, 1)

    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    cv2.imwrite('photo_away_machine.jpg',frame)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8883)
client.publish(topic, data) 

while True:
    while True:
        info = input("Do you want to send request? (Yes: Y)")
        if (info == 'Y'):
            client.publish(topic, info)
        else:
            break
        client.connect(brokerAddress, 8883)
        client.subscribe(topic)
        print("Waiting for Photo")
        client.loop_start()
        time.sleep(10)
        client.loop_stop()
