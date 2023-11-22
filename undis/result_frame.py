import os
from itertools import cycle
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import undis.util as util
from undis.asset import Asset
import color


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

    def handler_resize(self, event):
        self.configure(scrollregion=self.bbox(tk.ALL))
        self.__panel.configure(width=event.width - self.__scroll_bar.winfo_width())
        self.__panel.handler_resize_experimental(width=event.width - self.__scroll_bar.winfo_width())

    def handler_hover_enter(self, event):
        if util.Platform.detected() == util.Platform.Windows:
            self.winfo_toplevel().bind_all(sequence="<MouseWheel>", func=self.handler_mouse_wheel_windows)
        elif util.Platform.detected() == util.Platform.Linux:
            self.winfo_toplevel().bind_all(sequence="<Button-4>", func=self.handler_mouse_wheel_linux)
            self.winfo_toplevel().bind_all(sequence="<Button-5>", func=self.handler_mouse_wheel_linux)
        elif util.Platform.detected() == util.Platform.MacOS:
            self.winfo_toplevel().bind_all(sequence="<MouseWheel>", func=self.handler_mouse_wheel_macos)

    def handler_hover_exit(self, event):
        if util.Platform.detected() == util.Platform.Windows:
            self.winfo_toplevel().unbind_all(sequence="<MouseWheel>")
        elif util.Platform.detected() == util.Platform.Linux:
            self.winfo_toplevel().unbind_all(sequence="<Button-4>")
            self.winfo_toplevel().unbind_all(sequence="<Button-5>")
        elif util.Platform.detected() == util.Platform.MacOS:
            self.winfo_toplevel().unbind_all(sequence="<MouseWheel>")

    def handler_mouse_wheel_windows(self, event):
        self.yview_scroll(-1 * int(event.delta / 120), "units")

    def handler_mouse_wheel_macos(self, event):
        self.yview_scroll(int(event.delta), "units")
        pass

    def handler_mouse_wheel_linux(self, event):
        print(dir(event))
        if event.num == 4:
            self.yview_scroll(-1, "units")
        elif event.num == 5:
            self.yview_scroll(1, "units")
        pass


class InnerResultFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=color.DARK_BACKGROUND, **kwargs)

        self.column_count = 0
        self.row_count = 0
        self.__previous_width = 0

        self.image_buttons = [
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
            ImageButton(self, "/home/toroidalfox/test.png"),
        ]
        # TODO test code

        # self.bind(sequence="<Configure>", func=self.handler_resize)

    def destroy(self):
        super().destroy()

    def handler_resize_experimental(self, width):
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
        for column_index, image_button in zip(cycle(range(self.column_count)), self.image_buttons):
            image_button.grid(column=column_index, row=row_index)
            if column_index == self.column_count - 1:
                row_index += 1

        for column_index in range(new_column_count):
            self.grid_columnconfigure(column_index, minsize=ImageButton.actual_width(), pad=actual_padx)
        for row_index in range(self.row_count, new_row_count):
            self.grid_rowconfigure(row_index, minsize=ImageButton.actual_width() + 32, pad=8)

        self.column_count = new_column_count
        self.row_count = new_row_count

    def handler_resize(self, event):
        print(f"InnerFrame! {event.width}, {event.height}")
        if event.width == self.__previous_width:
            return
        else:
            self.__previous_width = event.width

        images_count = len(self.image_buttons)
        minimum_padx = 8

        new_column_count = max(
            1,
            int((event.width - minimum_padx) / (ImageButton.actual_width() + minimum_padx)),
        )
        new_row_count = images_count // new_column_count

        actual_padx = max(
            0,
            (event.width - ImageButton.actual_width() * new_column_count) / (new_column_count * 2),
        )

        row_index = 0
        for column_index, image_button in zip(cycle(range(self.column_count)), self.image_buttons):
            image_button.grid(column=column_index, row=row_index)
            if column_index == self.column_count - 1:
                row_index += 1

        for column_index in range(self.column_count, new_column_count):
            self.grid_columnconfigure(column_index, minsize=ImageButton.actual_width(), pad=actual_padx)
        for row_index in range(self.row_count, new_row_count):
            self.grid_rowconfigure(row_index, minsize=ImageButton.actual_width() + 32, pad=8)

        self.column_count = new_column_count
        self.row_count = new_row_count


class ImageButton(tk.Frame):
    __image_max_dimension = 256
    std_pad = 8

    @staticmethod
    def actual_width() -> int:
        return ImageButton.__image_max_dimension + ImageButton.std_pad * 2

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

        # call unload function to start from unloaded state
        self.unload_image()

        self.image_name_text = tk.Label(
            master=self,
            text=self.image_name,
            wraplength=ImageButton.__image_max_dimension,
            justify="center",
            fg=color.LIGHT_TEXT,
            padx=8,
            pady=8,
            borderwidth=0,
        )
        self.image_name_text.grid(row=1, column=0, sticky=tk.N + tk.S)
        self.grid_rowconfigure(1, weight=1)
        util.add_bindtag_to(bindtag_of=self, to=self.image_name_text)

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
        super().destroy()

    def load_image(self):
        image = Image.open(self.image_path)
        image.thumbnail(
            size=(self.__image_max_dimension, self.__image_max_dimension),
            resample=Image.BILINEAR,
        )
        self._image = ImageTk.PhotoImage(image=image, size=image.size)
        self.image_preview.configure(image=self._image)
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
