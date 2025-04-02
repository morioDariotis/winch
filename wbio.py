from threading import Timer, Thread
from models import Models, Direction
import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

DI_STATE_ADDRESS = 1250

class WBIOHandler():
    def __init__(self, models: Models):
        self.models = models
        self.encCWhalf = False
        self.encCCWhalf = False

    def open(self, port):
        thread = Thread(target = self.openThread, args = (port, ))
        thread.start()

    def openThread(self, port):
        #pymodbus_apply_logging_config("DEBUG")
        self.client = ModbusClient.ModbusSerialClient(
            port,
            framer=FramerType.RTU,
            #timeout=10,
            # retries=3,
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=2,
        )
        self.client.connect()
        try:
            response = self.client.read_holding_registers(DI_STATE_ADDRESS, count=16, slave=40)
            self.registersOld = response.registers
        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            self.client.close()
        

    def close(self):
        self.client.close()

    def updateModels(self, registers):
        for i, button in enumerate(self.models.userInputModel.buttons):
            if registers[i] % 2 == 1:
                button.push()
            if registers[i] % 2 == 0 and registers[i] - self.registersOld[i] == 1:
                button.release()
            if registers[i] % 2 == 0 and registers[i] - self.registersOld[i] >= 2:
                button.push()
                registers[i] -= 1
        enc0 = registers[6] - self.registersOld[6]
        enc1 = registers[7] - self.registersOld[7]
        if enc0 > 0 and enc1 == 0 and self.encCCWhalf == False:
            self.encCWhalf = True
        if enc1 > 0 and enc0 == 0 and self.encCWhalf == False:
            self.encCCWhalf = True
        if self.encCCWhalf == True and enc0 == 0 and enc1 == 0:
            self.models.winchModel.incHeight()
            self.encCCWhalf = False
        if self.encCWhalf == True and enc0 == 0 and enc1 == 0:
            self.models.winchModel.decHeight()
            self.encCWhalf = False
        
        self.registersOld = registers

    def read(self):
        thread = Thread(target = self.readThread)
        thread.start()

    def readThread(self):
        if not self.client.connected:
            return
        try:
            response = self.client.read_holding_registers(DI_STATE_ADDRESS, count=16, slave=40)
            self.updateModels(response.registers)
        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            self.client.close()
        self.startReading()

    def startReading(self):
        Timer(0.05, self.read).start()
        