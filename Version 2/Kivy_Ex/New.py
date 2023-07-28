import kivy
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text = "IoT 3D Printer App")
    
# if __name__ == "__main__" : kismini ekleyen de var!
MyApp().run()



