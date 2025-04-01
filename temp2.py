import multiprocessing
from customtkinter import *
from PIL import Image


class Loop():
    

    def __init__(self) -> None:
        pass
        
    def updateUI(self) -> None:
        Loop.image_label.place(x=0, y=50)
        Loop.image_label.update()
        Loop.label = CTkLabel(master=Loop.app, text="fsdfsfsdf")
        Loop.label.place(x=0, y=50)

    


if __name__ == "__main__":
    app = CTk()
    app.geometry("800x480")
        #app.wm_attributes('-type', 'splash')
    set_appearance_mode("dark")
    button_image = CTkImage(Image.open("winch.png"), size=(50, 50))
            
    image_label = CTkLabel(master=app, text="",image=button_image)
    image_label.place(x=700, y=50)
    app.update()
    print("dfjsdlf")
    while(1):
        app.update()

