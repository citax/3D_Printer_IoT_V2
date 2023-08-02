import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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
        # Arka planda çalışacak kodu buraya ekleyebilirsiniz

    def on_button1_press(self, instance):
        # Buton 1'e tıklanınca pop-up gösterme metodu çağrılır
        self.show_popup("Buton 1'e tıklandı!")

    def on_button2_press(self, instance):
        # Buton 2'ye tıklanınca pop-up gösterme metodu çağrılır
        self.show_popup("Buton 2'ye tıklandı!")

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
