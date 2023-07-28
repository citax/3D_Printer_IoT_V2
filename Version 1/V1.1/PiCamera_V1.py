from picamera import PiCamera
from time import sleep

camera = PiCamera()


camera.start_preview()
sleep(5)
camera.capture('/home/hertz/Desktop/The IoT 3D Printer Project/Photos/dragon.jpg')
camera.stop_preview()
