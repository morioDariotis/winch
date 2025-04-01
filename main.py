import asyncio
from visualisation import MainWindow
from manual import ManualControl
from simulation import WinchSimulator
from wbio import WBIOHandler
from auto import Point, AutoStateTarget, AutoTree
from models import Models, Direction

if __name__ == "__main__":
    models = Models()
    p0 = Point("WTP", 20)
    p1 = Point("TP", 0)
    a0 = AutoStateTarget(models, "Движение к точке ожидания", 0, 10, p0)
    a1 = AutoStateTarget(models, "Движение к верхней точке", 0, 10, p1)
    t = AutoTree()
    t.addState(a0)
    t.addState(a1)
    models.autoTrees.addTree(t)
    #sim = WinchSimulator(models)
    window = MainWindow(models)
    window.update()
    wbioh = WBIOHandler(models)
    wbioh.open('COM5')
    wbioh.startReading()
    models.winchModel.setHeight(4)
    models.winchModel.direction = Direction.down
    manualControl = ManualControl(models)
    while(1):
        manualControl.update()
        #sim.update()
        
        window.update()