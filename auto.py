from threading import Timer
from models import Models, Mode, AutoTrees, AutoTree, AutoState
from logger import Logger, LogLevel


class Point:
    def __init__(self, name, height) -> None:
        self.name: str = name
        self.height: float = height



class AutoStateTarget(AutoState):
    def __init__(self, models: Models, name, id, speed, target: Point) -> None:
        super().__init__(models, name, id, speed)
        self.target: Point = target

    def defineDirection(self):
        if self.target.height > self.models.winchModel.height:
            self.models.winchModel.turnDown()
        else:
            self.models.winchModel.turnUp()

    def start(self) -> None:
        super().start()
        self.defineDirection()
        

    def check(self) -> bool: 
        return self.target.height == self.models.winchModel.height

class AutoStateSleep(AutoState):
    def __init__(self) -> None:
        super().__init__()
        self.time: float
        self.bTimePassed = False

    def start(self) -> None:
        super().start()
        Timer(self.time, self.timePassed).start()

    def timePassed(self) -> None:
        self.bTimePassed = True

    def check(self) -> bool: 
        return self.bTimePassed

class AutoStateWait(AutoState):
    def __init__(self) -> None:
        super().__init__()



class AutoControl:
    def __init__(self, models):
        self.trees: list[AutoTree] = models.autoTrees.trees
        self.models = models
        

    def update(self):
        cur = self.models.autoTrees.currentTree
        tree = self.trees[cur].tree
        if not tree[cur].check():
            return
        self.models.autoTrees.currentState += 1
        self.models.autoTrees.currentState %= len(self.tree)
        tree[cur].start()
