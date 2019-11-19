from gpiozero import Button
from signal import pause

buttonPin = 16
button = Button(buttonPin)


def press():
    print("Button pressed!")


def release():
    print("Button released!")


button.when_pressed = press
button.when_released = release

pause()

