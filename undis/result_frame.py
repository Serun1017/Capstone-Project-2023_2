import os
from itertools import cycle
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from concurrent.futures import Future
import datetime

import undis.util as util
from undis.asset import Asset
import color
import image_loader


class ResultFrame(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=color.DARK_BACKGROUND, **kwargs)

        self.__scroll_bar = tk.Scrollbar(master=master, orient=tk.VERTICAL, command=self.yview)
        self.__panel = InnerResultFrame(master=self)

        self.configure(yscrollcommand=self.__scroll_bar.set)

        self.__scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.create_window((0, 0), window=self.__panel, anchor=tk.NW)

        # resize event
        self.bind(sequence="<Configure>", func=self.handler_resize)
        self.bind(sequence="<Enter>", func=self.handler_hover_enter)
        self.bind(sequence="<Leave>", func=self.handler_hover_exit)

    def get__panel(self):
        return self.__panel

    def handler_resize(self, event):
        self.configure(scrollregion=self.bbox(tk.ALL))
        self.__panel.configure(width=event.width - self.__scroll_bar.winfo_width())
        self.__panel.handler_resize_experimental(width=event.width - self.__scroll_bar.winfo_width(), master=self)

    def handler_hover_enter(self, _):
        if util.Platform.detected() == util.Platform.Windows:
            self.bind_all(sequence="<MouseWheel>", func=self.handler_mouse_wheel_windows)
        elif util.Platform.detected() == util.Platform.Linux:
            self.bind_all(sequence="<Button-4>", func=self.handler_mouse_wheel_linux)
            self.bind_all(sequence="<Button-5>", func=self.handler_mouse_wheel_linux)
        elif util.Platform.detected() == util.Platform.MacOS:
            self.bind_all(sequence="<MouseWheel>", func=self.handler_mouse_wheel_macos)

    def handler_hover_exit(self, _):
        if util.Platform.detected() == util.Platform.Windows:
            self.unbind_all(sequence="<MouseWheel>")
        elif util.Platform.detected() == util.Platform.Linux:
            self.unbind_all(sequence="<Button-4>")
            self.unbind_all(sequence="<Button-5>")
        elif util.Platform.detected() == util.Platform.MacOS:
            self.unbind_all(sequence="<MouseWheel>")

    def handler_mouse_wheel_windows(self, event):
        self.yview_scroll(-1 * int(event.delta / 120), "units")

    def handler_mouse_wheel_macos(self, event):
        self.yview_scroll(int(event.delta), "units")

    def handler_mouse_wheel_linux(self, event):
        if event.num == 4:
            self.yview_scroll(-1, "units")
        elif event.num == 5:
            self.yview_scroll(1, "units")


class InnerResultFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=color.DARK_BACKGROUND, **kwargs)

        self.column_count = 0
        self.row_count = 0
        self.__previous_width = 0

        self.workspace: str | None = None
        self.list_of_images = []
        self.image_buttons = []

    def update_workspace(self, workspace: str | None):
        self.workspace = workspace

        self.list_of_images = []
        for button in self.image_buttons:
            button.destroy()
        self.image_buttons = []

        if self.workspace is None:
            return

        for directory, subdirectories, files in os.walk(self.workspace):
            for file in files:
                if os.path.splitext(file)[1] in Asset.SUPPORTED_IMAGE_EXTENSIONS:
                    full_file_path = os.path.join(directory, file)
                    self.list_of_images.append(full_file_path)
                    self.image_buttons.append(ImageButton(self, full_file_path))

    def destroy(self):
        super().destroy()

    def handler_resize_experimental(self, width, master):
        if width == self.__previous_width:
            return
        else:
            self.__previous_width = width

        images_count = len(self.image_buttons)
        minimum_padx = 8

        new_column_count = max(1, int((width - minimum_padx) / (ImageButton.actual_width() + minimum_padx)))
        new_row_count = images_count // new_column_count

        actual_padx = max(0, (width - ImageButton.actual_width() * new_column_count) / new_column_count)

        row_index = 0
        for column_index, image_button in zip(cycle(range(new_column_count)), self.image_buttons):
            image_button.grid(column=column_index, row=row_index)
            if column_index == new_column_count - 1:
                row_index += 1

        for column_index in range(new_column_count):
            self.grid_columnconfigure(column_index, minsize=ImageButton.actual_width(), pad=actual_padx)
        for row_index in range(self.row_count, new_row_count):
            self.grid_rowconfigure(row_index, minsize=ImageButton.actual_width() + 32, pad=8)

        self.column_count = new_column_count
        self.row_count = new_row_count
        self.configure(height=self.row_count * (ImageButton.actual_width() + 32) + (self.row_count + 1) * 8)
        master.configure(scrollregion=master.bbox(tk.ALL))
        # print(
        #     f"height={self.row_count * (ImageButton.actual_width() + 32) + (self.row_count + 1) * 8}, bbox={master.bbox(tk.ALL)}"
        # )


class ImageButton(tk.Frame):
    IMAGE_MAX_DIMENSION = 256
    std_pad = 8

    @staticmethod
    def actual_width() -> int:
        return ImageButton.IMAGE_MAX_DIMENSION + ImageButton.std_pad * 2

    def __init__(self, master, image_path: str, **kwargs):
        super().__init__(
            master=master,
            borderwidth=0,
            **kwargs,
        )

        self.image_path = image_path
        self.image_name = os.path.basename(os.path.splitext(image_path)[0])

        self.image_preview = tk.Label(master=self, padx=0, pady=0, borderwidth=0)
        self.image_preview.grid(row=0, column=0, padx=ImageButton.std_pad, pady=ImageButton.std_pad)
        util.add_bindtag_to(bindtag_of=self, to=self.image_preview)

        self.image_name_text = tk.Label(
            master=self,
            text=self.image_name,
            wraplength=ImageButton.IMAGE_MAX_DIMENSION,
            justify="center",
            fg=color.LIGHT_TEXT,
            padx=8,
            pady=8,
            borderwidth=0,
        )
        self.image_name_text.grid(row=1, column=0, sticky=tk.N + tk.S)
        self.grid_rowconfigure(1, weight=1)
        util.add_bindtag_to(bindtag_of=self, to=self.image_name_text)

        self.image_loader_future = None

        # call unload function to start from unloaded state
        self.unload_image()

        # visibility event
        self.bind(sequence="<Visibility>", func=self.handler_visibility)
        # right click to open menu
        self.bind(sequence="<Button-3>", func=self.open_menu)
        # double click to open file
        self.bind(sequence="<Double-Button-1>", func=self.handler_double_click)
        # hover
        self.bind(sequence="<Enter>", func=self.handler_hover_enter)
        self.bind(sequence="<Leave>", func=self.handler_hover_exit)

        # call hover exit handler to set initial background color
        self.handler_hover_exit(None)

    def destroy(self):
        if self.image_loader_future is not None:
            self.image_loader_future.cancel()
        super().destroy()

    def load_image(self):
        self.image_loader_future = image_loader.image_loader.submit(load_image_future, self, self.image_path)
        self.image_loader_future.add_done_callback(self.__load_image_callback)

    def __load_image_callback(self, image_future: Future[Image.Image]):
        try:
            image = image_future.result(timeout=0)
        except Exception as _:
            self.image_loader_future = None
            return
        self._image = ImageTk.PhotoImage(image=image, size=strecth_image_size(image.size))
        self.image_preview.configure(image=self._image)
        self.image_loader_future = None
        self.image_loaded = True

    def unload_image(self):
        self._image = ImageTk.PhotoImage(image=Asset.EMPTY_IMAGE)
        self.image_preview.configure(image=self._image)
        self.image_loaded = False

    def open_file(self):
        util.file_open(self.image_path)

    def open_file_in_explorer(self, _event):
        util.file_open_in_explorer(self.image_path)

    def open_menu(self, event):
        menu = tk.Menu(tearoff=0)
        menu.config
        menu.add_command(label="Open File", command=lambda: util.file_open(self.image_path))
        menu.add_command(
            label="Reveal in File Explorer",
            command=lambda: util.file_open_in_explorer(self.image_path),
        )
        menu.tk_popup(event.x_root, event.y_root)

    def handler_visibility(self, event):
        if self.image_loaded is False and util.Visibility.is_state_visible(event.state):
            self.load_image()
        elif self.image_loaded is True and util.Visibility.is_state_obsucured(event.state):
            self.unload_image()

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


def strecth_image_size(size: tuple[int, int]) -> tuple[int, int]:
    width, height = size[0], size[1]
    max_dim = ImageButton.IMAGE_MAX_DIMENSION
    aspect_ratio = width / height
    if aspect_ratio > 1:
        return (int(max_dim * aspect_ratio), max_dim)
    else:
        return (max_dim, int(max_dim / aspect_ratio))


def load_image_future(image_button: ImageButton, image_path: str) -> Image.Image:
    try:
        image = Image.open(image_path)
        image.thumbnail(
            size=(ImageButton.IMAGE_MAX_DIMENSION, ImageButton.IMAGE_MAX_DIMENSION),
            resample=Image.BILINEAR,
        )
    except Exception as _:
        image = Asset.MISSING_IMAGE
    return image
