from tkinter import Canvas
import customtkinter


customtkinter.set_appearance_mode("system")

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


class ResultFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, width=Width / 2, height=Height, **kwargs)  # type: ignore


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("undis")
        self.resizable(True, True)
        make_button(self)

        self.frame = ResultFrame(self)
        self.make_canvas()
        self.frame.pack()

    def make_canvas(self):
        self.canvas = Canvas(self, width=Width / 2, height=Height + 100, bg="black")
        self.canvas.pack(
            side="left",
            fill="none",
        )


app = App()
app.geometry("1024x512")
app.mainloop()
