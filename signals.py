import pigpio
from threading import Timer
from models import Models

ENCODER_DELAY = 0.05

class Encoder():
    def __init__(self, models: Models, pi):
        self.models = models
        self.enc0 = False
        self.enc1 = False
        self.delay = False
        pi.callback(5, pigpio.FALLING_EDGE, self.enc0cb)
        pi.callback(6, pigpio.FALLING_EDGE, self.enc0cb)

    def delayOff(self):
        self.delay = False

    def enc0cb(self):
        if self.delay:
            return
        if self.enc1:
            self.models.winchModel.incHeight()
            self.delay = True
            self.enc1 = False
            Timer(ENCODER_DELAY, self.delayOff).start()
        else:
            self.enc0 = True

    def enc1cb(self):
        if self.delay:
            return
        if self.enc0:
            self.models.winchModel.decHeight()
            self.delay = True
            self.enc0 = False
            Timer(ENCODER_DELAY, self.delayOff).start()
        else:
            self.enc1 = True
    