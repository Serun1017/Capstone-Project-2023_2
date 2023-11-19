import os
import tkinter
import customtkinter as ctk
import utils
from PIL import Image


class ResultFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)


class ImageButton(ctk.CTkFrame):
    image_max_dimension = 512

    def __init__(self, master, image_path: str):
        super().__init__(master=master)

        self.image_path = image_path
        self.image_name = os.path.basename(os.path.splitext(image_path)[0])

        self.load_image()
        image = ctk.CTkLabel(self, image=self._image, text="")
        image.grid(row=0, column=0)
        # utils.add_bindtag_to(bindtag_of=self, to=image)
        image.bind(sequence="<Button-3>", command=lambda event: self.open_menu(event))

        # resize event
        self.bind(sequence="<Configure>", command=self.resize)
        # right click to open menu
        self.bind(sequence="<Button-3>", command=self.open_menu)
        # double click to open file
        self.bind(sequence="<Double-Button-1>", command=self.open_file)

    def load_image(self):
        image = image_resize(
            image=Image.open(self.image_path), max_dimension=self.image_max_dimension
        )
        self._image = ctk.CTkImage(light_image=image, size=image.size)

    def unload_image(self):
        self._image = None

    def resize(self, event):
        # TODO implement
        pass

    def open_file(self, _event):
        utils.file_open(self.image_path)

    def open_file_in_explorer(self, _event):
        utils.file_open_in_explorer(self.image_path)

    def open_menu(self, event):
        menu = tkinter.Menu(self, tearoff=0)
        menu.config
        menu.add_command(label="Open File", command=lambda: self.open_file(None))
        menu.add_command(
            label="Reveal in File Explorer",
            command=lambda: self.open_file_in_explorer(None),
        )
        menu.tk_popup(event.x_root, event.y_root)


def image_resize(image: Image.Image, max_dimension: int) -> Image.Image:
    """Resize an image to a max dimension while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height
    if aspect_ratio > 1:
        if width > max_dimension:
            width = max_dimension
            height = int(width / aspect_ratio)
            return image.resize(size=(width, height))
        else:
            return image
    elif height > max_dimension:
        if height > max_dimension:
            height = max_dimension
            width = int(height * aspect_ratio)
            return image.resize(size=(width, height))
        else:
            return image
    else:
        return image
