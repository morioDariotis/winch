import customtkinter as ctk
from PIL import Image
from models import Direction, Models
from auto import AutoTree

class AttributeWidget:
    def __init__(self, master, name, x, y) -> None:
        self.name = ctk.CTkButton(master=master, text=name, corner_radius=5, state="disabled", text_color_disabled="#FFFFFF")
        self.value = ctk.CTkButton(master=master, text=0, corner_radius=5, state="disabled", text_color_disabled="#FFFFFF")
        self.place(x, y)

    def place(self, x, y) -> None:
        self.name.place(x=x, y=y)
        self.value.place(x=x+160, y=y)

    def update(self, value) -> None:
        self.value.configure(text=value)

class LevelMark:
    def __init__(self, master, models: Models, text) -> None:
        self.models = models
        image = ctk.CTkImage(Image.open("resources/level_mark.png"), size=(50, 10))
        self.mark = ctk.CTkLabel(master=master, text=text,image=image, bg_color="transparent", height=10, width=50)

    def update(self, x, height) -> None:
        y = 50+round(300*(height/self.models.winchModel.maxHeight))
        self.mark.place(x=x, y=y)

class WinchImage:
    def __init__(self, master, x, y) -> None:
        image = ctk.CTkImage(Image.open("resources/winch.png"), size=(50, 300))
        self.winch = ctk.CTkLabel(master=master, text="",image=image)
        self.winch.place(x=x, y=y)

class Icon:
    def __init__(self, master, x, y, file) -> None:
        image = ctk.CTkImage(Image.open(file), size=(50, 50))
        self.icon = ctk.CTkLabel(master=master, text="",image=image)
        self.x = x
        self.y = y
        self.enabled = False  

    def update(self, isEnabled):
        if (isEnabled != self.enabled):
            self.enabled = isEnabled
            if isEnabled:
                self.icon.place(x=self.x, y=self.y)
            else:
                self.icon.place_forget()

class AutoTreeV:
    def __init__(self, tree: AutoTree, master):
        self.master = master
        self.tree = tree
        
    def draw(self):
        self.frame_tree = ctk.CTkFrame(self.master, fg_color="#1F1F1F")
        self.frame_tree.grid(row=0, column=0, padx=(20,20), sticky="nsew")
        for i, state in enumerate(self.tree.tree):
            frame_state = ctk.CTkFrame(self.frame_tree, fg_color="#292929")
            frame_state.grid(row=i, column=0, padx=(20,20), sticky="nsew")
            name = ctk.CTkLabel(frame_state, text=f"{state.name}")
            name.grid(row=0, column=1, padx=(20,20), sticky="nsew")
            button_up = ctk.CTkButton(frame_state, text="вверх", corner_radius=5, command= lambda: self.tree.moveState(i, -1))
            button_up.grid(row=0, column=0, padx=(20,20), sticky="nsew")
            button_down = ctk.CTkButton(frame_state, text="ввниз", corner_radius=5, command= lambda: self.tree.moveState(i, 1))
            button_down.grid(row=1, column=0, padx=(20,20), sticky="nsew")



class MainWindow:
    def __init__(self, models) -> None:
        self.models = models
        self.master = ctk.CTk()
        self.master.geometry("800x480")
        ctk.set_appearance_mode("dark")
        self.tabview = ctk.CTkTabview(master=self.master, width=800, height=480)
        self.drawInfo()
        self.drawConf()
        self.drawAuto()
        self.tabview.pack()

    def updateWidgets(self) -> None:
        self.updateInfo()
        self.updateConf()
        self.updateAuto()

    def drawInfo(self) -> None:
        self.infoTab = self.tabview.add("Монитор")
        self.height = AttributeWidget(self.infoTab, "Глубина", 10, 50)
        self.power = AttributeWidget(self.infoTab, "Мощность", 10, 80)
        self.winch = WinchImage(self.infoTab, 700, 50)
        self.upIcon = Icon(self.infoTab, 500, 50, "resources/up.png")
        self.stopIcon = Icon(self.infoTab, 500, 50, "resources/stop.png")
        self.downIcon = Icon(self.infoTab, 500, 50, "resources/down.png")
        self.currentHeightMark = LevelMark(self.infoTab, self.models, "Высота")
        self.wtp = LevelMark(self.infoTab, self.models, "WTP")
        self.wdp = LevelMark(self.infoTab, self.models, "WDP")


    def updateInfo(self) -> None:
        self.height.update(self.models.winchModel.heightM)
        self.power.update(self.models.winchModel.heightM)
        self.currentHeightMark.update(700, self.models.winchModel.height)
        self.wtp.update(650, 1)
        self.wdp.update(650, 23)
        if (self.models.winchModel.direction == Direction.stop):
            self.upIcon.update(False)
            self.stopIcon.update(True)
            self.downIcon.update(False)
        if (self.models.winchModel.direction == Direction.up):
            self.upIcon.update(True)
            self.stopIcon.update(False)
            self.downIcon.update(False)
        if (self.models.winchModel.direction == Direction.down):
            self.upIcon.update(False)
            self.stopIcon.update(False)
            self.downIcon.update(True)

    def drawConf(self) -> None:
        self.confTab = self.tabview.add("Конфигурация")
    
    def updateConf(self) -> None:
        pass

    def drawAuto(self) -> None:
        self.autoTab = self.tabview.add("Автоматический режим")
        self.autoV = AutoTreeV(self.models.autoTrees.trees[self.models.autoTrees.currentTree], self.autoTab)
        self.autoV.draw()

    def updateAuto(self) -> None:
        if self.autoV.tree.update:
            self.autoV.draw()
            self.autoV.tree.update = False

    def update(self) -> None:
        self.updateWidgets()
        self.master.update()


