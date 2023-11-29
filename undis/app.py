import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from concurrent.futures import Future
from PIL import Image

import cv2
import torch
import numpy as np
from torchvision.transforms import transforms
from .sbir_mod.data_utils.utils import remove_white_space_image, resize_image_by_ratio, make_img_square

from . import color
from .asset import Asset, asset_loader
from .components import result_frame
from . import draw_canvas


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("undis")
        self.resizable(True, True)
        self.minsize(720, 512)

        self.configure(bg=color.DARK_BACKGROUND)

        self.workspace: str | None = None

        self.menu_construct()

        self.panel = result_frame.ResultFrame(master=self)
        self.panel.pack(side="right", fill=tk.BOTH, expand=True)

        # self.panel.pack(side="right", fill="both", expand=True)
        self.Canvas_layer = draw_canvas.DrawCanvas(self, 512, 512)
        self.Canvas_layer.pack(fill=tk.BOTH)

        self.button_panel = ctk.CTkFrame(master=self)
        self.buttons(master=self.button_panel)
        self.button_panel.pack(fill=tk.BOTH, expand=True)

        # self.clear_button()
        # self.retrieve_image_button()
        # self.erase_button()
        # self.pen_button()

    def destroy(self):
        asset_loader.shutdown(wait=False, cancel_futures=True)
        super().destroy()

    def open_workspace(self):
        retrieved_workspace = filedialog.askdirectory()
        if retrieved_workspace == ():
            return
        self.workspace = retrieved_workspace
        self.panel.update_workspace(self.workspace)

    def retrieve_images_with_sketch(self):
        self.sketch = np.array(self.Canvas_layer.render_as_image())
        self.image_data_list = self.panel.get_list_of_tokens()

        self.sketch_tokenized = False
        self.sketch_tokens = transforms.Tensor

        self.sk_future = asset_loader.submit(tokenize_sketch_data, Asset.MODEL.result(), self.sketch)
        self.sk_future.add_done_callback(self.__tokenize_sketch_callback)

    def __tokenize_sketch_callback(self, sk_future: Future[Image.Image]):
        try:
            self.sk_tokenized_data = sk_future.result(timeout=0)
            self.is_sk_tokenized = True

            self.rn = asset_loader.submit(
                cross_attention, Asset.MODEL.result(), self.sk_tokenized_data, self.image_data_list
            )
            self.rn.add_done_callback(self.__after_cross_attention)  # type: ignore
        except Exception as _:
            self.sk_tokenized_data = None
            self.is_sk_tokenized = False

    def __after_cross_attention(self, rn: Future[Image.Image]):
        try:
            self.panel.sort_by_result(rn.result(timeout=0))  # type: ignore
            # print(self.result)
        except Exception as _:
            self.result = None

    def menu_construct(self):
        if getattr(self, "_menu_constructed", False) is True:
            return

        # menu
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(self, tearoff=False)

        # menu_bar
        menu_bar.add_cascade(label="File", menu=file_menu)

        # file_menu
        file_menu.add_command(label="Open Workspace", command=self.open_workspace)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

        self.configure(menu=menu_bar)
        self._menu_constructed = True

    def buttons(self, master):
        draw_mode_var = tk.IntVar(value=0)
        brush_button = ctk.CTkRadioButton(
            master, text="brush", variable=draw_mode_var, value=0, command=self.Canvas_layer.bind_pen
        )
        brush_button.grid(column=0, row=0)
        eraser_button = ctk.CTkRadioButton(
            master, text="eraser", variable=draw_mode_var, value=1, command=self.Canvas_layer.bind_eraser
        )
        eraser_button.grid(column=1, row=0)

        clear_button = ctk.CTkButton(master, text="clear", command=self.Canvas_layer.clear)
        clear_button.grid(column=2, row=0, sticky=tk.E)
        retrieve_button = ctk.CTkButton(
            master,
            text="retrieve",
            command=self.retrieve_images_with_sketch,
        )
        retrieve_button.grid(column=2, row=100, sticky=tk.SE)
        master.grid_columnconfigure(2, weight=1)
        master.grid_rowconfigure(100, weight=1)


# Load sk_data (numpy array) and preprocecss the sketch.
def tokenize_sketch_data(model, sketch):
    sk_data = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)

    immean = [0.5, 0.5, 0.5]  # RGB channel mean for imagenet
    imstd = [0.5, 0.5, 0.5]

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(immean, imstd)])

    sk_data = remove_white_space_image(sk_data, 10)
    sk_data = resize_image_by_ratio(sk_data, 224)
    sk_data = make_img_square(sk_data)

    sk_data = transform(sk_data).half()  # type: ignore
    sk_data = torch.unsqueeze(sk_data, 0)
    sk_data = sk_data.cuda()

    sk_data, _ = model(sk_data, None, "test", only_sa=True)

    return sk_data


def cross_attention(model, sketch_data, image_buttons: list[tuple[str, transforms.Tensor]]):
    labels = np.array([])
    dist_im = []

    initialized = False
    for image_path, tokens in image_buttons:
        labels = np.append(labels, image_path)

        sk_temp = sketch_data.unsqueeze(1).repeat(1, 1, 1, 1).flatten(0, 1).cuda()
        im_temp = tokens.unsqueeze(0).repeat(1, 1, 1, 1).flatten(0, 1).cuda()  # type: ignore
        feature_1, feature_2 = model(sk_temp, im_temp, "test")

        if initialized is False:
            dist_im = feature_2.view(1, 1).cpu().data.numpy()  # 1*args.batch
            initialized = True
        else:
            dist_im = np.concatenate((dist_im, feature_2.view(1, 1).cpu().data.numpy()), axis=1)  # type: ignore

    dist_im = np.squeeze(dist_im)

    sorted_indices = np.argsort(dist_im)
    sorted_indices = sorted_indices[::-1]

    dist_im = dist_im[sorted_indices]
    labels = labels[sorted_indices]

    result = np.stack([dist_im, labels])

    print(result)
    return result
