import tkinter
from tkinter import Canvas
import customtkinter
import result_frame
import draw_canvas

import undis.color as color
from undis.asset import Asset
import undis.asset as asset


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("theme.json")
customtkinter.set_window_scaling(1.5)

Width = 1024
Height = 600


def test_callback():
    print("what")


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y
    pass


def make_button(self):
    self.playbutton = customtkinter.CTkButton(self, text="play", command=test_callback)
    self.playbutton.place(x=50)
    self.playbutton.pack(side="left", anchor="nw")

    pass


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__(fg_color=color.DARK_BACKGROUND)
        self.title("undis")
        self.resizable(True, True)
        self.minsize(512, 512)

        self.workspace: str | None = None

        panel = result_frame.ResultFrame(master=self)
        panel.pack(side="right", fill="both", expand=True)

        Canvas_layer = draw_canvas.DrawCanvas(self, Width, Height)
        Canvas_layer.pack(side="left", fill="both")
        Canvas_layer.bind("<Button-1>", Canvas_layer.get_x_and_y)
        Canvas_layer.bind("<B1-Motion>", Canvas_layer.draw_some)


app = App()
app.geometry("1024x600")
app.mainloop()

# tip
# use dir() function to dump everything of object
