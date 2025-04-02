from threading import Timer, Thread
from models import Models, Direction
import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

CONTROL_REGISTER_ADDRESS = 0x2000
FREQUENCY_REGISTER_ADDRESS = 0x2001
STOP_VALUE = 0x0001
UP_VALUE = 0x0022
DOWN_VALUE = 0x0012




class FMHandler():
    def __init__(self, models: Models, slave: int):
        self.models = models
        self.slave: int = slave

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
            stopbits=1,
        )
        self.client.connect()
        print("connected")

    def close(self):
        self.client.close()


    def sendData(self, address, data):
        try:
            self.client.write_register(address, data, slave=self.slave, no_response_expected=False)
        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            self.client.close()

    def readData(self, address, count):
        try:
            response = self.client.read_holding_registers(address, count, slave=self.slave, no_response_expected=False)
            return response.registers
        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            self.client.close()
            return -1
        
    def stop(self):
        self.sendData(CONTROL_REGISTER_ADDRESS, STOP_VALUE)

    def down(self):
        self.sendData(CONTROL_REGISTER_ADDRESS, DOWN_VALUE)

    def up(self):
        self.sendData(CONTROL_REGISTER_ADDRESS, UP_VALUE)

    def setSpeed(self, speed):
        self.sendData(FREQUENCY_REGISTER_ADDRESS, speed)

    def update(self):
        if not self.models.winchModel.needUpdate:
            return
        self.setSpeed(self.models.winchModel.speed)
        if self.models.winchModel.direction == Direction.down:
            self.down()
        if self.models.winchModel.direction == Direction.up:
            self.up()
        if self.models.winchModel.direction == Direction.stop:
            self.stop()
            self.setSpeed(0)
        
        self.models.winchModel.needUpdate = False
