import os
from itertools import cycle
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter

import undis.util as util
from undis.asset import Asset
import color


class ResultFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, fg_color=color.DARK_BACKGROUND, **kwargs)

        self.column_count = 1

        self.image_buttons = [
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-hourglass-twins-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-timber-hearth-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-hourglass-twins-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-timber-hearth-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-hourglass-twins-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-timber-hearth-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-hourglass-twins-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-timber-hearth-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-hourglass-twins-4x.jpg",
            ),
            ImageButton(
                self,
                "/home/toroidalfox/GoogleDrive/Pictures/background/outer-wilds-landscape/clement-campargue-timber-hearth-4x.jpg",
            ),
        ]
        # TODO test code

        self.bind(sequence="<Configure>", func=self.handler_resize)

    def handler_resize(self, event):
        self.column_count = int(event.width / 256)
        for column_index in range(self.column_count):
            self.grid_columnconfigure(index=column_index, minsize=256)

        row_index = 0
        for column_index, image_button in zip(
            cycle(range(self.column_count)), self.image_buttons
        ):
            image_button.grid(column=column_index, row=row_index, padx=8, pady=8)
            if column_index == self.column_count - 1:
                row_index += 1

        pass


class ImageButton(tk.Frame):
    image_max_dimension = 256

    def __init__(self, master, image_path: str, **kwargs):
        super().__init__(master=master, **kwargs)

        self.image_path = image_path
        self.image_name = os.path.basename(os.path.splitext(image_path)[0])

        self.unload_image()
        self.image_loaded = False

        # image = ctk.CTkLabel(self, image=self._image, text="")
        # image.grid(row=0, column=0)
        # utils.add_bindtag_to(bindtag_of=self, to=image)
        self.image_preview = tk.Label(master=self, image=self._image)
        self.image_preview.grid(row=0, column=0)
        util.add_bindtag_to(bindtag_of=self, to=self.image_preview)

        self.image_name_text = tk.Label(
            master=self,
            text=self.image_name,
            wraplength=256,
            justify="center",
            fg=color.LIGHT_TEXT,
        )
        self.image_name_text.grid(row=1, column=0)
        util.add_bindtag_to(bindtag_of=self, to=self.image_name_text)

        # visibility event
        self.bind(sequence="<Visibility>", func=self.handler_visibility)
        # resize event
        self.bind(sequence="<Configure>", func=self.handler_resize)
        # right click to open menu
        self.bind(sequence="<Button-3>", func=self.open_menu)
        # double click to open file
        self.bind(sequence="<Double-Button-1>", func=self.handler_double_click)
        # hover
        self.bind(sequence="<Enter>", func=self.handler_hover_enter)
        self.bind(sequence="<Leave>", func=self.handler_hover_exit)

        # call hover exit handler to set initial background color
        self.handler_hover_exit(None)

    def load_image(self):
        image = Image.open(self.image_path)
        image.thumbnail(
            size=(self.image_max_dimension, self.image_max_dimension),
            resample=Image.BILINEAR,
        )
        self._image = ImageTk.PhotoImage(image=image, size=image.size)
        self.image_preview.configure(image=self._image)
        self.image_loaded = True

    def unload_image(self):
        self._image = ImageTk.PhotoImage(image=Asset.EMPTY_IMAGE)
        self.image_loaded = False

    def open_file(self):
        util.file_open(self.image_path)

    def open_file_in_explorer(self, _event):
        util.file_open_in_explorer(self.image_path)

    def open_menu(self, event):
        menu = tk.Menu(self, tearoff=0, bg=color.DARK_BACKGROUND, fg=color.LIGHT_TEXT)
        menu.config
        menu.add_command(
            label="Open File", command=lambda: util.file_open(self.image_path)
        )
        menu.add_command(
            label="Reveal in File Explorer",
            command=lambda: util.file_open_in_explorer(self.image_path),
        )
        menu.tk_popup(event.x_root, event.y_root)

    def handler_visibility(self, event):
        if self.image_loaded is False and util.Visibility.is_state_visible(event.state):
            self.load_image()
        elif self.image_loaded is True and util.Visibility.is_state_obsucured(
            event.state
        ):
            self.unload_image()

    def handler_resize(self, event):
        print(f"resize of {self.image_name[-12:-1]}: {event.width}, {event.height}")
        # TODO implement
        pass

    def handler_double_click(self, _):
        self.open_file()

    def handler_hover_enter(self, _):
        for child in self.winfo_children():
            child.configure(bg=color.DARK_BACKGROUND_HOVER)  # type: ignore
        self.configure(bg=color.DARK_BACKGROUND_HOVER)

    def handler_hover_exit(self, _):
        for child in self.winfo_children():
            child.configure(bg=color.DARK_BACKGROUND)  # type: ignore
        self.configure(bg=color.DARK_BACKGROUND)


# def image_resize(image: Image.Image, max_dimension: int) -> None:
#     """Resize an image to a max dimension while maintaining aspect ratio."""
#     width, height = image.size
#     aspect_ratio = width / height
#     if aspect_ratio > 1:
#         if width > max_dimension:
#             width = max_dimension
#             height = int(width / aspect_ratio)
#             return image.thumbnail(size=(width, height), resample=Image.BILINEAR)
#         else:
#             return image
#     elif height > max_dimension:
#         if height > max_dimension:
#             height = max_dimension
#             width = int(height * aspect_ratio)
#             return image.resize(size=(width, height))
#         else:
#             return image
#     else:
#         return image
