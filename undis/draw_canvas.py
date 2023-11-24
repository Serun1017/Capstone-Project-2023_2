import tkinter
from PIL import Image
import numpy as np


class DrawCanvas(tkinter.Canvas):
    def __init__(self, master, w, h):
        super().__init__(master=master, width=w, height=h, bg="white")

        self.brush_width = 16
        self.brush_tip_radius = max(self.brush_width // 2 - 1, 0)

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

    # 지금은 line과 oval을 이용해서 부드러운 선을 그리고 있음. create_line의 join style과 capstyle을 이용하면 된다는 것을 알아챔.
    # 실행취소는 find_all()에서 delete(id:int)를 이용해서 구현할 수 있을 것 같음.
    # 지우개는 하얀색 칠하기 보다 find_overlapping() 혹은 find_closest()를 이용하면 될 것 같음.

    def save(self):
        self.postscript(file="image")
        img = Image.open("image")
        img2 = np.array(img)
        print(img2)

    def debug(self):
        print("canvas debug dump")
        for child in self.find_all():
            print(child)
        print(self.type(1))
        print(self.coords(1))

    def erase(self, event):
        target_object_ids = self.find_overlapping(event.x - 4, event.y - 4, event.x + 4, event.y + 4)
        for target_object_id in target_object_ids:
            self.delete(target_object_id)
