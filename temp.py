from datetime import datetime

class Model:
    def __init__(self) -> None:
        self.attr = 0

    def inc(self):
        self.attr += 1

    def dec(self):
        self.attr -= 1


class First:
    def __init__(self, model) -> None:
        self.model = model

    def inc(self):
        self.model.inc()

class Second:
    def __init__(self, model) -> None:
        self.model = model

    def inc(self):
        self.model.inc()

if __name__ == "__main__":
    now = datetime.now().strftime("%H:%M:%S")
    print(now)


