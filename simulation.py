from models import Models, Direction
import threading
import time
import keyboard

class WinchSimulator:
    def __init__(self, models: Models) -> None:
        self.models = models
        self.busy: bool = False
        

    def stepUp(self):
        time.sleep(1)
        self.busy = False
        self.models.winchModel.incHeight()
        print("stepUp")
        

    def stepDown(self):
        time.sleep(1)
        self.busy = False
        self.models.winchModel.decHeight()
        print("stepDown")

    def operate(self) -> None:
        if self.busy: 
            return
        if (self.models.winchModel.direction == Direction.up):
            print("trying to go up")
            threading.Timer(1, self.stepUp).start()
            self.busy = True
        if (self.models.winchModel.direction == Direction.down):
            print("trying to go down")
            threading.Timer(1, self.stepDown).start()
            self.busy = True

    def userInput(self) -> None:
        for button in self.models.userInputModel.buttons:
            button.release()
        if keyboard.is_pressed('q'):
            exit(1)
        if keyboard.is_pressed('w'):
            self.models.userInputModel.buttonUp.push()
        if keyboard.is_pressed('s'):
            self.models.userInputModel.buttonDown.push()
        if keyboard.is_pressed('m'):
            self.models.userInputModel.buttonManual.push()
        if keyboard.is_pressed('p'):
            self.models.userInputModel.buttonPush.push()
        if keyboard.is_pressed('a'):
            self.models.userInputModel.buttonAuto.push()

    def update(self):
        self.userInput()
        self.operate()

