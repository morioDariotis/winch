from models import Models

class Event():
    def __init__(self):
        self.checkInManual = False
        self.checkInAuto = True
        self.checkInPush = False



class ObstacleUp(Event):
    def __init__(self):
        super().__init__()
        self.handlers = []

    def check(self):
        return False

    def addHandler(self):
        self.handlers.append(self.Handler())

    def update(self):
        if self.check():
            self.addHandler()
        for handle in self.handlers:
            if handle.update():
                del handle
        
    class Handler():
        def __init__(self):
            pass

        def update():
            pass

        

    
class EventListener():
    def __init__(self):
        self.events = []

    def listen(self):
        for event in self.events:
            event.update()