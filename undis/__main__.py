from tkinter import *
import tkinter as tk
from PIL import Image


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_some(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y), fill="black", width=2)
    lasx, lasy = event.x, event.y


def save_img(event):
    ##image = ImageGrab.grab( )
    canvas.postscript(file="dra.ps")
    img = Image.open("dra.ps")
    img.save("dra.jpg", "JPEG", path="C:\\Users\\82105\\source\\repos\\CreateCanvas")


window = tk.Tk()

window.geometry("1024x1024")
window.resizable(True, True)

canvas = Canvas(window, bg="white")

canvas.pack(anchor="nw", fill="both", expand=1)

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_some)
canvas.bind("<Button-3>", save_img)

canvas.update()

window.mainloop()
