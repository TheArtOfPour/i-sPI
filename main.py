#!~/i-sPI/.venv/bin python

from gpiozero import Button
from signal import pause
from picamera import PiCamera
from time import sleep
from image_detection import ImageDetection

button_pin = 16
model_dir = 'Sample_TFLite_model'
image_path = '/tmp/picture.jpg'

button = Button(button_pin)
camera = PiCamera()
detector = ImageDetection(model_dir)
print("ready")


def press():
    camera.start_preview()
    sleep(1)
    camera.capture(image_path)
    camera.stop_preview()
    detector.detect(image_path)


def release():
    print("released")


button.when_pressed = press
button.when_released = release

pause()
