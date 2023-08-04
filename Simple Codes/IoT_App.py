import kivy
import cv2
import paho.mqtt.client as mqtt
import time
import numpy as np
import base64
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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

kivy.require('1.11.1')  # Kivy sürümünü belirtin (bu kod örneği için en az 1.11.1 sürümü gereklidir)

class MinimalistApp(App):
    def build(self):
        # Ana düzen
        layout = FloatLayout()

        # İlk buton
        button1 = Button(text='Buton 1', size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        button1.bind(on_press=self.on_button1_press)
        layout.add_widget(button1)

        # İkinci buton
        button2 = Button(text='Buton 2', size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        button2.bind(on_press=self.on_button2_press)
        layout.add_widget(button2)

        # Uygulama başlatıldığında çalıştırılacak kod
        self.on_start_app()

        return layout

    def on_start_app(self):
        # Uygulama başlatıldığında çalışacak kod buraya gelecek
        print("Uygulama başlatıldı!")

        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set(userName, passWord)
        client.connect(brokerAddress, 8883)
        client.publish(topic, data) 
        
        # Arka planda çalışacak kodu buraya ekleyebilirsiniz

    def on_button1_press(self, instance):
        # Buton 1'e tıklanınca pop-up gösterme metodu çağrılır
        self.show_popup("Buton 1'e tıklandı!")


    def on_button2_press(self, instance):
        # Buton 2'ye tıklanınca pop-up gösterme metodu çağrılır
        # self.show_popup("Buton 2'ye tıklandı!")
        info = "Y"
        client.publish(topic, info)
        client.connect(brokerAddress, 8883)
        client.subscribe(topic)
        print("Waiting for Photo")
        client.loop_start()
        time.sleep(10)
        client.loop_stop()

    def show_popup(self, message):
        # Pop-up içeriği
        content = FloatLayout()
        content.add_widget(Label(text=message))
        content.add_widget(Button(text='Kapat', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'y': 0.1}, on_press=self.close_popup))

        # Pop-up penceresi
        popup = Popup(title='Bildirim', content=content, size_hint=(None, None), size=(400, 200), auto_dismiss=False)
        self.current_popup = popup  # pop-up referansını sakla
        popup.open()

    def close_popup(self, instance):
        # Pop-up penceresini kapatma metodu
        self.current_popup.dismiss()

if __name__ == '__main__':
    MinimalistApp().run()
