import RPi.GPIO as GPIO
from models import Models

ENC0_PIN = 10
ENC1_PIN = 10


class GPIO_Handler:
    def __init__(self, models: Models):
        self.models = models
        self.encCWhalf = False
        self.encCCWhalf = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENC0_PIN, GPIO.IN)
        GPIO.setup(ENC1_PIN, GPIO.IN)
        GPIO.add_event_detect(ENC0_PIN, GPIO.RISING,
                      callback=self.interrupt_handler,
                      bouncetime=20)
        GPIO.add_event_detect(ENC1_PIN, GPIO.RISING,
                      callback=self.interrupt_handler,
                      bouncetime=20)

    def interrupt_handler(self, pin):
        if pin == ENC0_PIN:
            if GPIO.input(ENC1_PIN):
                self.models.winchModel.incHeight()
        elif pin == ENC1_PIN:
            if GPIO.input(ENC0_PIN):
                self.models.winchModel.decHeight()