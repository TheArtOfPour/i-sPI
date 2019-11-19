# import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause

buttonPin = 16
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button = Button(buttonPin)


# def button_press(channel):
#     print("Button pressed!")


def press():
    print("Button pressed!")


def release():
    print("Button pressed!")


button.when_pressed = press
button.when_released = release

# GPIO.add_event_detect(24, GPIO.RISING, callback=button_press, bouncetime=300)

# condition = True
# while condition:
#     time.sleep(300)

pause()

# raw_input("Listening...")
# GPIO.cleanup()
