import tkinter as tk
from tkinter import filedialog

import color
import result_frame

import os
from os import listdir

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
        Canvas_layer = draw_canvas.DrawCanvas(self, Width, Height)
        Canvas_layer.pack(side="left", fill="both")

    def open_workspace(self):
        self.image_routes = []
        self.workspace = filedialog.askdirectory()
        temp_workspace = self.workspace
        for images in os.listdir(self.workspace):
            if images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jepg"):
                self.workspace = temp_workspace + "/" + images
                self.image_routes.append(self.workspace)
                self.panel.get__panel().add_image(self.workspace)

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
