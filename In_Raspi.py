import cv2
import paho.mqtt.client as mqtt
import time
import base64
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
role_pin = 21
GPIO.setup(role_pin, GPIO.OUT)

brokerAddress = "*********************************************"
userName = "****************"
passWord = "****************"
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
        time.sleep(5)
        ret, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        cv2.imwrite('photo_in_raspi.jpg',frame)
        cap.release()
        client.publish(topic, jpg_as_text)

    elif (info == 'O') :
        GPIO.output(role_pin, GPIO.HIGH)

    elif (info == 'C'):
        GPIO.output(role_pin, GPIO.LOW)

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

