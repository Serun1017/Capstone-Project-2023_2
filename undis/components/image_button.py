import math
import os
from concurrent.futures import Future
import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from typing import Self

import torch
from torchvision.transforms import transforms

from .. import color
from ..asset import Asset, asset_loader
from .. import util


class ImageButton(tk.Frame):
    IMAGE_MAX_DIMENSION = 256
    PADDING = 8

    @staticmethod
    def actual_width() -> int:
        return ImageButton.IMAGE_MAX_DIMENSION + ImageButton.PADDING * 2

    @staticmethod
    def actual_height() -> int:
        return ImageButton.actual_width() + tkfont.Font(font="TkDefaultFont").metrics("linespace") * 2

    def __init__(self, master, image_path: str, **kwargs):
        super().__init__(
            master=master,
            borderwidth=0,
            bg=color.DARK_BACKGROUND,
            **kwargs,
        )
        self.image_path = image_path
        self.image_name = os.path.basename(os.path.splitext(self.image_path)[0])
        self.score: float = 1

        self.image_loader_future = None
        self.tokenize_image_future = None
        self.image_loaded = False
        self.is_image_tokenized = False

        self.tokenized_image = transforms.Tensor

        self.__inner_frame = _InnerFrame(master=self, text=self.image_name, borderwidth=0)
        self.__inner_frame.pack()
        self.load_image(self.image_path)

        self.__inner_frame.bind(sequence="<Button-3>", func=self.handler_right_click)
        self.__inner_frame.bind(sequence="<Double-Button-1>", func=self.handler_double_left_click)
        self.__inner_frame.bind(sequence="<Enter>", func=self.handler_hover_enter)
        self.__inner_frame.bind(sequence="<Leave>", func=self.handler_hover_exit)
        self.handler_hover_exit(None)  # start from non-hover state

    def __lt__(self, other: Self) -> bool:
        return self.score < other.score

    def __le__(self, other: Self) -> bool:
        return self.score <= other.score

    def __gt__(self, other: Self) -> bool:
        return self.score > other.score

    def __ge__(self, other: Self) -> bool:
        return self.score >= other.score

    def destroy(self):
        # if self.image_loader_future is not None:
        #     self.image_loader_future.cancel()
        # if self.tokenize_image_future is not None:
        #     self.tokenize_image_future.cancel()
        super().destroy()

    def unload_image(self):
        self.__inner_frame.set_image(image=ImageTk.PhotoImage(image=Asset.EMPTY_IMAGE, size=Asset.EMPTY_IMAGE.size))
        self.image_loaded = False

    def load_image(self, image_path: str):
        """Starts loading image in a thread pool."""
        self.image_loader_future = asset_loader.submit(load_image_task, image_path)
        self.image_loader_future.add_done_callback(self.__load_image_callback)

    def __load_image_callback(self, image_future: Future[Image.Image]):
        try:
            image = image_future.result(timeout=0)
            self.__inner_frame.set_image(image=ImageTk.PhotoImage(image=image, size=stretch_image_size(image.size)))
            self.image_loader_future = None
            self.image_loaded = True

            self.tokenize_image_future = asset_loader.submit(SelfAttention, image, Asset.MODEL.result())
            self.tokenize_image_future.add_done_callback(self.__image_tokenize_callback)
        except Exception as _:
            self.image_loader_future = None
            return

    def __image_tokenize_callback(self, tokenized_image: Future[Image.Image]):
        try:
            self.tokenized_image = tokenized_image.result()
            self.is_image_tokenized = True
            self.tokenize_image_future = None
        except Exception as _:
            self.tokenize_image_future = None
            self.tokenized_image = None
            self.is_image_tokenized = False
            return

    def handler_double_left_click(self, event):
        """Double left click to open file"""
        util.file_open(self.image_path)

    def handler_right_click(self, event):
        """Right click to open menu"""
        menu = tk.Menu(tearoff=0)
        menu.config
        menu.add_command(label="Open File", command=lambda: util.file_open(self.image_path))
        menu.add_command(
            label="Reveal in File Explorer",
            command=lambda: util.file_open_in_explorer(self.image_path),
        )
        menu.tk_popup(event.x_root, event.y_root)

    def handler_hover_enter(self, _):
        """Hover enter to change background color"""
        for child in self.__inner_frame.winfo_children():
            child.configure(bg=color.DARK_BACKGROUND_HOVER)  # type: ignore
        self.__inner_frame.configure(bg=color.DARK_BACKGROUND_HOVER)

    def handler_hover_exit(self, _):
        """Hover exit to change background color back to normal"""
        for child in self.__inner_frame.winfo_children():
            child.configure(bg=color.DARK_BACKGROUND)  # type: ignore
        self.__inner_frame.configure(bg=color.DARK_BACKGROUND)


class _InnerFrame(tk.Frame):
    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master=master,
            **kwargs,
        )
        self.image_frame = tk.Frame(master=self, padx=ImageButton.PADDING, pady=ImageButton.PADDING, borderwidth=0)
        self.image_frame.grid(column=0, row=0)
        util.add_bindtag_to(bindtag_of=self, to=self.image_frame)
        self.image_label = tk.Label(master=self.image_frame, padx=0, pady=0, borderwidth=0)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        util.add_bindtag_to(bindtag_of=self, to=self.image_label)

        self.image_name_text = tk.Label(
            master=self,
            text=text,
            wraplength=ImageButton.IMAGE_MAX_DIMENSION,
            justify=tk.CENTER,
            fg=color.LIGHT_TEXT,
            padx=ImageButton.PADDING,
            pady=ImageButton.PADDING,
            borderwidth=0,
        )
        self.image_name_text.grid(row=1, column=0, sticky=tk.N)
        util.add_bindtag_to(bindtag_of=self, to=self.image_name_text)

    def set_image(self, image: ImageTk.PhotoImage):
        self.__image = image
        self.image_label.configure(image=self.__image)


def stretch_image_size(size: tuple[int, int]) -> tuple[int, int]:
    width, height = size[0], size[1]
    max_dim = ImageButton.IMAGE_MAX_DIMENSION
    aspect_ratio = width / height
    if aspect_ratio > 1:
        return (int(max_dim * aspect_ratio), max_dim)
    else:
        return (max_dim, int(max_dim / aspect_ratio))


def load_image_task(image_path: str) -> Image.Image:
    try:
        image = Image.open(image_path)

        image.thumbnail(
            size=(ImageButton.IMAGE_MAX_DIMENSION, ImageButton.IMAGE_MAX_DIMENSION),
            resample=Image.BILINEAR,
        )

    except Exception as _:
        image = Asset.MISSING_IMAGE

    return image


def SelfAttention(image, model):
    immean = [0.5, 0.5, 0.5]  # RGB channel mean for imagenet
    imstd = [0.5, 0.5, 0.5]
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(immean, imstd)])
    tokenized_image = transform(image.resize((224, 224)).convert("RGB"))
    tokenized_image = tokenized_image.half()
    tokenized_image = torch.unsqueeze(tokenized_image, 0)

    tokenized_image = tokenized_image.cuda()
    tokenized_image, _ = model(tokenized_image, None, "test", only_sa=True)

    return tokenized_image
