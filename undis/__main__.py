import tkinter as tk
from tkinter import filedialog
import customtkinter
import result_frame
import draw_canvas

import color
from asset import Asset


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("theme.json")

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


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__(fg_color=color.DARK_BACKGROUND)
#         self.title("undis")
#         self.resizable(True, True)
#         self.minsize(512, 512)

#         self.workspace: str | None = None

#         # make_button(self)

#         # self.make_canvas()

#         panel = result_frame.ResultFrame(master=self)
#         panel.pack(fill="both", expand=True)

#     def make_canvas(self):
#         self.canvas = Canvas(self, width=Width / 2, height=Height + 100, bg="black")
#         self.canvas.pack(
#             side="left",
#             fill="none",
#         )


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("undis")
        self.resizable(True, True)
        self.minsize(512, 512)

        self.configure(bg=color.DARK_BACKGROUND)

        self.workspace: str | None = None

        self.menu_construct()

        panel = result_frame.ResultFrame(master=self)
        panel.pack(side="right", fill="both", expand=True)

        Canvas_layer = draw_canvas.DrawCanvas(self, Width, Height)
        Canvas_layer.pack(side="left", fill="both")

    def open_workspace(self):
        self.workspace = filedialog.askdirectory()

    def menu_construct(self):
        if getattr(self, "_menu_constructed", False) is True:
            return

        # menu
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(self, tearoff=False)

        # menu_bar
        menu_bar.add_cascade(label="File", menu=file_menu)

        # file_menu
        file_menu.add_command(label="Open Workspace", command=self.open_workspace)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

        self.configure(menu=menu_bar)
        self._menu_constructed = True


app = App()
app.geometry("1536x1024")
app.mainloop()

# tip
# use dir() function to dump everything of object
