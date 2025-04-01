from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    Info = 0
    Error = 1

class Logger:
    def __init__(self) -> None:
        pass

    @staticmethod
    def log(message: str, level: LogLevel):
        print(f'[{datetime.now().strftime("%H:%M:%S")}]({level.name}): {message}')