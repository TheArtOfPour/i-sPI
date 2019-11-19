#!~/i-sPI/.venv/bin python

from gpiozero import Button
from signal import pause
from picamera import PiCamera
from time import sleep

buttonPin = 16
button = Button(buttonPin)
camera = PiCamera()


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
