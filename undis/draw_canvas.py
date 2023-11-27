import tkinter
from PIL import Image
import numpy as np
import cv2
import torch
import io

from module.data_utils.utils import remove_white_space_image, resize_image_by_ratio, make_img_square
from torchvision.transforms import transforms
from . import image_loader
from concurrent.futures import Future
from .result_frame import ImageButton
from typing import List


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

    def retrieve_image(self, model, image_data_list: List[ImageButton]):
        ps = self.postscript(colormode="color")
        image = Image.open(io.BytesIO(ps.encode("utf-8")))

        self.model = model
        self.image_data_list = image_data_list

        self.sk_data = np.array(image)
        self.is_sk_tokenized = False
        self.sk_tokenized_data = transforms.Tensor

        self.sk_future = image_loader.image_loader.submit(tokenize_sketch_data, self.model, self.sk_data)
        self.sk_future.add_done_callback(self.__tokenize_sketch_callback)

    def __tokenize_sketch_callback(self, sk_future: Future[Image.Image]):
        try:
            self.sk_tokenized_data = sk_future.result(timeout=0)
            self.is_sk_tokenized = True

            self.rn = image_loader.image_loader.submit(
                cross_attention, self.model, self.sk_tokenized_data, self.image_data_list
            )
            self.rn.add_done_callback(self.__cross_attention)
        except Exception as _:
            self.sk_tokenized_data = None
            self.is_sk_tokenized = False

    def __cross_attention(self, rn: Future[Image.Image]):
        try:
            self.result = rn.result(timeout=0)
        except Exception as _:
            self.result = None

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


# Load sk_data (numpy array) and preprocecss the sketch.
def tokenize_sketch_data(model, sketch):
    sk_data = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)

    immean = [0.5, 0.5, 0.5]  # RGB channel mean for imagenet
    imstd = [0.5, 0.5, 0.5]

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(immean, imstd)])

    sk_data = remove_white_space_image(sk_data, 10)
    sk_data = resize_image_by_ratio(sk_data, 224)
    sk_data = make_img_square(sk_data)

    sk_data = transform(sk_data).half()
    sk_data = torch.unsqueeze(sk_data, 0)
    sk_data = sk_data.cuda()

    sk_data, _ = model(sk_data, None, "test", only_sa=True)

    return sk_data


def cross_attention(model, sketch_data, image_data_list: List[ImageButton]):
    labels = np.array([])
    dist_im = []

    for i, image_data in enumerate(image_data_list):
        if image_data.is_image_tokenized == True:
            labels = np.append(labels, image_data.image_path)

            sk_temp = sketch_data.unsqueeze(1).repeat(1, 1, 1, 1).flatten(0, 1).cuda()
            im_temp = image_data.tokenized_image.unsqueeze(0).repeat(1, 1, 1, 1).flatten(0, 1).cuda()  # type: ignore
            feature_1, feature_2 = model(sk_temp, im_temp, "test")

            if i == 0:
                dist_im = feature_2.view(1, 1).cpu().data.numpy()  # 1*args.batch
            else:
                dist_im = np.concatenate((dist_im, feature_2.view(1, 1).cpu().data.numpy()), axis=1)  # type: ignore

        else:
            image_data_list.append(image_data)
    dist_im = np.squeeze(dist_im)

    sorted_indices = np.argsort(dist_im)
    sorted_indices = sorted_indices[::-1]

    dist_im = dist_im[sorted_indices]
    labels = labels[sorted_indices]

    result = np.stack([dist_im, labels])

    print(result)
    return result
