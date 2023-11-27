import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk


from . import color
from .components import result_frame
from . import draw_canvas


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("undis")
        self.resizable(True, True)
        self.minsize(512, 512)

        self.configure(bg=color.DARK_BACKGROUND)

        self.workspace: str | None = None

        self.menu_construct()

        self.panel = result_frame.ResultFrame(master=self)

        self.panel.pack(side="right", fill="both", expand=True)
        self.Canvas_layer = draw_canvas.DrawCanvas(self, 512, 512)
        self.Canvas_layer.pack(fill="both")

        self.clear_button()
        self.retrieve_image_button()
        self.erase_button()
        self.pen_button()

    def open_workspace(self):
        retrieved_workspace = filedialog.askdirectory()
        if retrieved_workspace == ():
            return
        self.workspace = retrieved_workspace
        self.panel.update_workspace(self.workspace)

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

    def clear_button(self):
        self.playbutton = ctk.CTkButton(self, text="clear", command=self.Canvas_layer.clear)
        self.playbutton.place(x=50)
        self.playbutton.pack(side="left", anchor="nw")

    def retrieve_image_button(self):
        self.playbutton = ctk.CTkButton(
            self,
            text="retrieve",
            command=lambda: self.Canvas_layer.retrieve_image(self.panel.get_list_of_images()),
        )
        self.playbutton.place(x=80)
        self.playbutton.pack(side="left", anchor="nw")

    def erase_button(self):
        self.playbutton = ctk.CTkButton(self, text="erase", command=self.Canvas_layer.bind_eraser)
        self.playbutton.place(x=110)
        self.playbutton.pack(side="left", anchor="nw")

    def pen_button(self):
        self.playbutton = ctk.CTkButton(self, text="pen", command=self.Canvas_layer.bind_pen)
        self.playbutton.place(x=130)
        self.playbutton.pack(side="left", anchor="nw")
