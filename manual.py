from models import Models, Mode
from logger import Logger, LogLevel

class ManualControl:
    def __init__(self, models: Models) -> None:
        self.models = models

    def manual(self) -> None:
        if (self.models.userInputModel.buttonUp.getState()):
            self.models.winchModel.turnUp()
        if (self.models.userInputModel.buttonDown.getState()):
            self.models.winchModel.turnDown()
        if (self.models.userInputModel.buttonStop.getState()):
            self.models.winchModel.stop()
        

    def auto(self) -> None:
        self.models.winchModel.stop()

    def push(self) -> None:
        if (self.models.userInputModel.buttonUp.getState()):
            self.models.winchModel.turnUp()
        elif (self.models.userInputModel.buttonDown.getState()):
            self.models.winchModel.turnDown()
        else:
            self.models.winchModel.stop()

    def switch(self) -> None:
        if (self.models.userInputModel.buttonPush.getState()):
            if (self.models.systemState.modeState != Mode.push):
                self.models.systemState.modeState = Mode.push
                Logger.log("Switched to push mode", LogLevel.Info)
        if (self.models.userInputModel.buttonManual.getState()):
            if (self.models.systemState.modeState != Mode.manual):
                self.models.systemState.modeState = Mode.manual
                Logger.log("Switched to manual mode", LogLevel.Info)
        if (self.models.userInputModel.buttonAuto.getState()):
            if (self.models.systemState.modeState != Mode.auto):
                self.models.systemState.modeState = Mode.auto
                Logger.log("Switched to auto mode", LogLevel.Info)

    def update(self) -> None:
        self.switch()
        if (self.models.systemState.modeState == Mode.push):
            self.push()
        if (self.models.systemState.modeState == Mode.manual):
            self.manual()
        if (self.models.systemState.modeState == Mode.auto):
            self.auto()