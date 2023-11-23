import tkinter
from PIL import Image
import numpy as np


class DrawCanvas(tkinter.Canvas):
    def __init__(self, master, w, h):
        super().__init__(master=master, width=w, height=h, bg="white")

        self.brush_width = 16
        self.brush_tip_radius = max(self.brush_width // 2 - 1, 0)

        self.bind("<Button-1>", self.get_x_and_y)
        self.bind("<B1-Motion>", self.draw_some)

    def get_x_and_y(self, event):
        global lasx, lasy
        self.create_oval(
            event.x - self.brush_tip_radius,
            event.y - self.brush_tip_radius,
            event.x + self.brush_tip_radius,
            event.y + self.brush_tip_radius,
            fill="black",
        )
        lasx, lasy = event.x, event.y

    def draw_some(self, event):
        global lasx, lasy
        self.create_line((lasx, lasy, event.x, event.y), fill="black", width=self.brush_width)
        self.create_oval(
            event.x - self.brush_tip_radius,
            event.y - self.brush_tip_radius,
            event.x + self.brush_tip_radius,
            event.y + self.brush_tip_radius,
            fill="black",
        )
        lasx, lasy = event.x, event.y

    def clear(self):
        self.delete("all")

    def save(self):
        self.postscript(file="image")
        img = Image.open("image")
        img2 = np.array(img)
        print(img2)
