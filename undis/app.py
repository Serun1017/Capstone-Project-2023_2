import tkinter as tk
from tkinter import filedialog
import customtkinter

from asset import Asset
import color
import result_frame

import os

import draw_canvas

Width = 600
Height = 600


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
        self.Canvas_layer = draw_canvas.DrawCanvas(self, Width, Height)
        self.Canvas_layer.pack(fill="both")

        self.clear_button()
        self.save_button()

    def open_workspace(self):
        self.workspace = filedialog.askdirectory()
        self.panel.get__panel().update_workspace(self.workspace)

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
        self.playbutton = customtkinter.CTkButton(self, text="clear", command=self.Canvas_layer.clear)
        self.playbutton.place(x=50)
        self.playbutton.pack(side="left", anchor="nw")

    def save_button(self):
        self.playbutton = customtkinter.CTkButton(self, text="save", command=self.Canvas_layer.save)
        self.playbutton.place(x=80)
        self.playbutton.pack(side="left", anchor="nw")
