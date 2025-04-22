from enum import Enum

HEIGHT_SCALE_FACTOR = 0.4
HEIGHT_MAX = 25

class Direction(Enum):
    stop = 0
    up = 1
    down = 2

class Rotation(Enum):
    unchanged = 0
    cw = 1
    ccw = 2

class Mode(Enum):
    manual = 0
    push = 1
    auto = 2

class WinchModel():
    def __init__(self) -> None:
        self.height: int = 0 
        self.scaleFactor: float = HEIGHT_SCALE_FACTOR
        self.maxHeight: float = HEIGHT_MAX
        self.heightM: float = 0
        self.direction: Direction = Direction.stop
        self.speed: int = 1000
        self.needUpdate: bool = False

    def scaleHeight(self) -> None:
        self.heightM = round(self.height * self.scaleFactor, 2)

    def incHeight(self) -> None:
        self.height += 1
        self.scaleHeight()

    def decHeight(self) -> None:
        self.height -= 1
        self.scaleHeight()

    def setHeight(self, height: int) -> None:
        self.height = height
        self.scaleHeight()
    
    def turnUp(self) -> None:
        if self.direction == Direction.up:
            return
        self.direction = Direction.up
        self.needUpdate = True

    def turnDown(self) -> None:
        if self.direction == Direction.down:
            return
        self.direction = Direction.down
        
        self.needUpdate = True

    def stop(self) -> None:
        if self.direction == Direction.stop:
            return
        self.direction = Direction.stop
        self.needUpdate = True

    def setSpeed(self, speed) -> None:
        if self.speed == speed:
            return
        self.speed = speed
        self.needUpdate = True

class RotationSensorModel():
    def __init__(self) -> None:
        self.state = Rotation.unchanged
    
    def rotationCW(self) -> None:
        self.state = Rotation.cw

    def rotationCCW(self) -> None:
        self.state = Rotation.ccw

    def rotationUnchanged(self) -> None:
        self.state = Rotation.unchanged

class ZeroPointSensorModel():
    def __init__(self) -> None:
        self.zeroPoint = False
    
    def set(self) -> None:
        self.zeroPoint = True

    def reset(self) -> None:
        self.zeroPoint = False

class TensionSensorModel():
    def __init__(self) -> None:
        self.looseTension = False

    def set(self) -> None:
        self.looseTension = True

    def reset(self) -> None:
        self.looseTension = False

class PowerThresholdModel():
    def __init__(self) -> None:
        self.highPower = False

    def set(self) -> None:
        self.highPower = True

    def reset(self) -> None:
        self.highPower = False

class Button():
    def __init__(self) -> None:
        self.state = False

    def push(self) -> None:
        self.state = True

    def release(self) -> None:
        self.state = False

    def getState(self) -> bool:
        return self.state

class UserInputModel():
    def __init__(self) -> None:
        self.buttonUp = Button()
        self.buttonStop = Button()
        self.buttonDown = Button()
        self.buttonManual = Button()
        self.buttonAuto = Button()
        self.buttonPush = Button()
        self.buttons = [self.buttonUp,self.buttonStop,self.buttonDown,self.buttonManual,self.buttonAuto,self.buttonPush]

class SystemState():
    def __init__(self) -> None:
        self.errorState = 0
        self.winchState = 0
        self.autoState = 0
        self.modeState = Mode.auto

class Settings():
    def __init__(self) -> None:
        pass

class AutoState:
    def __init__(self, models, name, id, speed) -> None:
        self.name: str = name
        self.id: int = id
        self.speed: float = speed
        self.models: Models = models

    def start(self) -> None:
        self.models.winchModel.speed = self.speed

class AutoTree:
    def __init__(self) -> None:
        self.tree: list[AutoState] = []
        self.update = True

    def addState(self, state: AutoState) -> None:
        self.tree.append(state)

    def moveState(self, id, value) -> None:
        sId = (id + value) % len(self.tree)
        if sId < 0 : sId = 0
        self.tree[id].id = sId
        self.tree[sId].id = id
        self.tree.sort(key= lambda x: x.id)
        self.update = True


class AutoTrees():
    def __init__(self):
        self.currentTree: int = 0
        self.currentState: int = -1
        self.trees: list[AutoTree] = []

    def addTree(self, tree: AutoTree):
        self.trees.append(tree)


class Models:
    def __init__(self) -> None:
        self.winchModel = WinchModel()
        self.rotationSensorModel = RotationSensorModel()
        self.zeroPointSensorModel = ZeroPointSensorModel()
        self.tensionSensorModel = TensionSensorModel()
        self.powerThresholdModel = PowerThresholdModel()
        self.userInputModel = UserInputModel()
        self.systemState = SystemState()
        self.settings = Settings()
        self.autoTrees = AutoTrees()
