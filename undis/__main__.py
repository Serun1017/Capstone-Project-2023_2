import tkinter
from tkinter import Canvas
import customtkinter
import result_frame

import undis.color as color
from undis.asset import Asset
import undis.asset as asset


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("theme.json")
customtkinter.set_window_scaling(1.5)

Width = 1024
Height = 512


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

        # make_button(self)

        # self.make_canvas()

        panel = result_frame.ResultFrame(master=self)
        panel.pack(fill="both", expand=True)

    def make_canvas(self):
        self.canvas = Canvas(self, width=Width / 2, height=Height + 100, bg="black")
        self.canvas.pack(
            side="left",
            fill="none",
        )


app = App()
app.geometry("1024x600")
app.mainloop()

# tip
# use dir() function to dump everything of object
