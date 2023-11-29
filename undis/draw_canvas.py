import tkinter
from PIL import Image

import io


class DrawCanvas(tkinter.Canvas):
    def __init__(self, master, w, h):
        super().__init__(master=master, width=w, height=h, bg="white")

        self.brush_width = 8

        self.bind_pen()

    def bind_pen(self):
        self.unbind("<Button-1>")
        self.unbind("<B1-Motion>")
        self.bind("<Button-1>", self.get_x_and_y)
        self.bind("<B1-Motion>", self.draw_some)

    def bind_eraser(self):
        self.unbind("<Button-1>")
        self.unbind("<B1-Motion>")
        self.bind("<Button-1>", self.erase)
        self.bind("<B1-Motion>", self.erase)

    def get_x_and_y(self, event):
        global lasx, lasy
        lasx, lasy = event.x, event.y
        self.stroke_id = self.create_line(
            (event.x, event.y, event.x, event.y),
            fill="black",
            width=self.brush_width,
            joinstyle="round",
            capstyle="round",
        )

    def draw_some(self, event):
        global lasx, lasy
        coordinates = self.coords(self.stroke_id)
        coordinates.append(event.x)
        coordinates.append(event.y)
        self.coords(self.stroke_id, coordinates)
        lasx, lasy = event.x, event.y

    def clear(self):
        self.delete(tkinter.ALL)

    def render_as_image(self) -> Image.Image:
        return Image.open(io.BytesIO(self.postscript(colormode="color").encode("utf-8")))

    def debug(self):
        print("canvas debug dump")
        for child in self.find_all():
            print(child)
        print(self.type(1))
        print(self.coords(1))

    def erase(self, event):
        target_object_ids = self.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        for target_object_id in target_object_ids:
            self.delete(target_object_id)
