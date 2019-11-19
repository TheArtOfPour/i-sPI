#!~/i-sPI/.venv/bin python

from gpiozero import Button
from signal import pause
from picamera import PiCamera
from time import sleep
from image_detection import ImageDetection

button_pin = 16
model_dir = 'Sample_TFLite_model'

button = Button(button_pin)
camera = PiCamera()
detector = ImageDetection(model_dir)


def press():
    camera.start_preview()
    sleep(1)
    camera.capture('/tmp/picture.jpg')
    camera.stop_preview()


def release():
    print("released")


button.when_pressed = press
button.when_released = release

pause()
