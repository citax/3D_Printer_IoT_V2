import kivy
import os
import cv2
import paho.mqtt.client as mqtt
import time
import numpy as np
import base64
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
from kivy.uix.popup import Popup
from kivy.uix.label import Label

brokerAddress = "*************************"
userName = "*************************"
passWord = "*************************"
topic = "my/test/topic"
data = "Hello from Away Machine"

current_directory = os.getcwd()
photo_path = current_directory + '\photo.jpg'

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
   
    Photo_Name = 'photo.jpg'
    cv2.imwrite(Photo_Name,frame)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

class MinimalistApp(App):
    def build(self):
        # Ana düzen
        self.layout = FloatLayout()
        self.image = Image(pos_hint={'center_x': 0.7, 'center_y': 0.5}, size_hint=(0.5, 0.4),
                           allow_stretch=True, keep_ratio=True)  # allow_stretch ve keep_ratio özellikleri eklendi
        self.layout.add_widget(self.image)

        # Load Photo Button
        button1 = Button(text='Load Photo', size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.2, 'center_y': 0.6})
        button1.bind(on_press=self.on_button1_press)
        self.layout.add_widget(button1)

        # Send Request Button
        button2 = Button(text='Send Request', size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.2, 'center_y': 0.8})
        button2.bind(on_press=self.on_button2_press)
        self.layout.add_widget(button2)

        # Refresh Button
        button3 = Button(text='Refresh Photo', size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.2, 'center_y': 0.4})
        button3.bind(on_press=self.on_button3_press)
        self.layout.add_widget(button3)

        # GPIO On/Off Button
        button4 = Button(text='GPIO On/Off', size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.2, 'center_y': 0.2})
        button4.bind(on_press=self.on_button4_press)
        self.layout.add_widget(button4)

        # Uygulama başlatıldığında çalıştırılacak kod
        self.on_start_app()

        return self.layout
        

    def refresh_photo(self, instance):
        # Burada mevcut fotoğrafı yenileme işlemini gerçekleştirebilirsiniz
        # Yenileme işlemini fotoğrafı tekrar yükleyerek yapacağım.

        self.load_photo(None)

    def on_start_app(self):
        # Uygulama başlatıldığında çalışacak kod buraya gelecek
        print("Program is Starting..")

        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set(userName, passWord)
        client.connect(brokerAddress, 8883)
        client.publish(topic, data) 
        
        # Arka planda çalışacak kodu buraya ekleyebilirsiniz

    def on_button1_press(self, instance):                       
        # Photo Load Button.                       
        # Burada fotoğraf yükleme işlemini gerçekleştirebilirsiniz
        # Örneğin, dosya seçme iletkisi kullanabilirsiniz.
        # Benim örneğimde, mevcut bir fotoğrafı kullanıyorum.

        # Fotoğrafın yolunu ve adını düzenleyin
        
        # Kivy Image nesnesine fotoğrafı yükle
        pil_image = PILImage.open(photo_path)
        pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)
        pil_image = pil_image.resize((800, 600))  # Resmi daha büyük yapmak için boyutu arttırdık
        buf = pil_image.tobytes()
        texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = texture


    def on_button2_press(self, instance):
        # Send Request Button.
        info = "Y"
        client.publish(topic, info)
        client.connect(brokerAddress, 8883)
        client.subscribe(topic)
        print("Waiting for Photo")
        client.loop_start()
        time.sleep(10)
        client.loop_stop()

    def on_button3_press(self, instance):
        # Refresh Photo Button.
        self.on_button1_press(None)

    def on_button4_press(self, instance):
        # GPIO On/Off Button.
        self.show_popup("")

    def show_popup(self, message):
        # Pop-up içeriği
        content = FloatLayout()
        content.add_widget(Label(text=message))
        content.add_widget(Button(text='Kapat', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'y': 0.1}, on_press=self.close_popup))

        # Pop-up penceresi
        popup = Popup(title='Show Photo', content=content, size_hint=(None, None), size=(400, 200), auto_dismiss=False)
        self.current_popup = popup  # pop-up referansını sakla
        popup.open()

    def close_popup(self, instance):
        # Pop-up penceresini kapatma metodu
        self.current_popup.dismiss()

if __name__ == '__main__':
    MinimalistApp().run()
