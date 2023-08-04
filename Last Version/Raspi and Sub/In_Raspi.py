import cv2
import paho.mqtt.client as mqtt
import time
import base64

brokerAddress = "12a52b54af3f4191912ad167a7925c0e.s1.eu.hivemq.cloud"
userName = "citak"
passWord = "275452Ahmet"
topic = "my/test/topic"
data = "Hello From Raspi"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

def on_message(client, userdata, msg):
    info = msg.payload.decode()
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    if (info == 'Y') :
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        cv2.imwrite('photo_in_raspi.jpg',frame)
        cap.release()
        client.publish(topic, jpg_as_text)

print("Program Started")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8883)
client.publish(topic, data) 
client.subscribe(topic)
client.loop_forever()
