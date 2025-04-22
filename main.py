import asyncio
from visualisation import MainWindow
from manual import ManualControl
from simulation import WinchSimulator
from auto import Point, AutoStateTarget, AutoTree
from models import Models, Direction
from fm import FMHandler
from auto import AutoControl
import time
from signals import Encoder
import pigpio

if __name__ == "__main__":
    models = Models()
    p0 = Point("WTP", 20)
    p1 = Point("TP", 0)
    p2 = Point("DP", 60)
    a0 = AutoStateTarget(models, "Движение к точке ожидания", 0, 1000, p0)
    a1 = AutoStateTarget(models, "Движение к верхней точке", 1, 800, p1)
    a2 = AutoStateTarget(models, "Движение к нижней точке", 2, 1200, p2)
    t = AutoTree()
    t.addState(a0)
    t.addState(a1)
    t.addState(a2)
    models.autoTrees.addTree(t)
    window = MainWindow(models)
    window.update()
    pi = pigpio.pi()
    enc = Encoder(models, pi)
    fmh = FMHandler(models, 5)
    fmh.open("COM7")
    time.sleep(2)
    manualControl = ManualControl(models)
    autoControl = AutoControl(models)
    while(1):
        manualControl.update()
        fmh.update()
        autoControl.update()
        window.update()