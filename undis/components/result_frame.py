import os
from itertools import cycle
import tkinter as tk
from torchvision.transforms import transforms

from .. import color
from ..asset import Asset
from .. import util
from .image_button import ImageButton


class ResultFrame(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=color.DARK_BACKGROUND, **kwargs)

        self.workspace: str | None = None
        self.list_of_images: list[str] = []

        self.__scroll_bar = tk.Scrollbar(master=master, orient=tk.VERTICAL, command=self.yview)
        self.__inner_frame = InnerResultFrame(master=self)
        self.configure(yscrollcommand=self.__scroll_bar.set)
        self.__scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.create_window((0, 0), window=self.__inner_frame, anchor=tk.NW)

        # resize event
        self.bind(sequence="<Configure>", func=self.handler_resize)
        self.bind(sequence="<Enter>", func=self.handler_hover_enter)
        self.bind(sequence="<Leave>", func=self.handler_hover_exit)

    def update_workspace(self, workspace: str | None):
        self.workspace = workspace

        self.list_of_images = []
        if self.workspace is None:
            return

        for directory, _, files in os.walk(self.workspace):
            files.sort()  # TODO: delete later. sorting is only for testing
            for file in files:
                if os.path.splitext(file)[1] in Asset.SUPPORTED_IMAGE_EXTENSIONS:
                    full_file_path = os.path.join(directory, file)
                    self.list_of_images.append(full_file_path)

        self.__inner_frame.create_buttons_from_list_of_images(self.list_of_images)
        self.__inner_frame.explicit_config(width=self.__inner_frame.winfo_width(), override=True, master=self)
        self.configure(scrollregion=self.bbox(tk.ALL))

    def sort_by_result(self, result: list[list[str]]):
        scores, image_paths = result[0], result[1]
        image_buttons = self.__inner_frame.get_image_buttons()
        for score, image_path in zip(scores, image_paths):
            for image_button in filter(lambda x: x.image_path == image_path, image_buttons):
                image_button.score = float(score)
        self.__inner_frame.explicit_config(width=self.__inner_frame.winfo_width(), override=True, master=self)
        self.configure(scrollregion=self.bbox(tk.ALL))

    def get_list_of_tokens(self) -> list[tuple[str, transforms.Tensor]]:
        list_of_images = []
        for image_button in self.__inner_frame.get_image_buttons():
            list_of_images.append((image_button.image_path, image_button.tokenized_image))
        return list_of_images

    def handler_resize(self, event):
        self.__inner_frame.configure(width=event.width - self.__scroll_bar.winfo_width())
        self.__inner_frame.explicit_config(width=event.width - self.__scroll_bar.winfo_width())
        self.configure(scrollregion=self.bbox(tk.ALL))

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

        self.row_count = 0
        self.__previous_width = 0

        self.threshold: float = 0.6
        self.__image_buttons: list[ImageButton] = []

    def create_buttons_from_list_of_images(self, list_of_images: list[str]):
        for button in self.__image_buttons:
            button.destroy()
        self.__image_buttons = []

        for image_path in list_of_images:
            image_button = ImageButton(master=self, image_path=image_path)
            self.__image_buttons.append(image_button)

    def destroy(self):
        super().destroy()

    def get_image_buttons(self) -> list[ImageButton]:
        return self.__image_buttons

    def explicit_config(self, width: int, override: bool = False, master=None):
        if width == self.__previous_width and override is False:
            return
        else:
            self.__previous_width = width

        for image_button in self.__image_buttons:
            image_button.grid_remove()

        minimum_padx = ImageButton.PADDING

        new_column_count = max(1, int((width - minimum_padx) / (ImageButton.actual_width() + minimum_padx)))

        actual_padx = max(0, (width - ImageButton.actual_width() * new_column_count) / new_column_count)

        row_count = 0
        for column_index, image_button in zip(
            cycle(range(new_column_count)),
            sorted(filter(lambda x: x.score > self.threshold, self.__image_buttons), reverse=True),
        ):
            image_button.grid(column=column_index, row=row_count)
            if column_index == new_column_count - 1:
                column_index = 0
                row_count += 1

        for column_index in range(new_column_count):
            self.grid_columnconfigure(column_index, minsize=ImageButton.actual_width(), pad=actual_padx)
        for row_count in range(row_count):
            self.grid_rowconfigure(row_count, minsize=ImageButton.actual_height(), pad=ImageButton.PADDING)

        total_height = row_count * ImageButton.actual_height() + (row_count + 1) * ImageButton.PADDING + 1024
        self.configure(height=total_height)
        if master is not None:
            master.configure(height=total_height)
