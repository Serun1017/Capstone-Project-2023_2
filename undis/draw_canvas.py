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

class DrawCanvas(tkinter.Canvas):
    def __init__(self, master, w, h):
        super().__init__(master=master, width=w, height=h, bg="white")

        self.brush_width = 16
        self.brush_tip_radius = max(self.brush_width // 2 - 1, 0)

        self.bind("<Button-1>", self.get_x_and_y)
        self.bind("<B1-Motion>", self.draw_some)

    def get_x_and_y(self, event):
        global lasx, lasy
        self.create_oval(
            event.x - self.brush_tip_radius,
            event.y - self.brush_tip_radius,
            event.x + self.brush_tip_radius,
            event.y + self.brush_tip_radius,
            fill="black",
        )
        lasx, lasy = event.x, event.y

    def draw_some(self, event):
        global lasx, lasy
        self.create_line((lasx, lasy, event.x, event.y), fill="black", width=self.brush_width)
        self.create_oval(
            event.x - self.brush_tip_radius,
            event.y - self.brush_tip_radius,
            event.x + self.brush_tip_radius,
            event.y + self.brush_tip_radius,
            fill="black",
        )
        lasx, lasy = event.x, event.y

    def clear(self):
        self.delete(tkinter.ALL)
        # test code. remove later
        self.create_line(
            [(0, 0), (100, 100), (200, 100), (200, 200)], fill="black", width=16, joinstyle="round", capstyle="round"
        )

    # 지금은 line과 oval을 이용해서 부드러운 선을 그리고 있음. create_line의 join style과 capstyle을 이용하면 된다는 것을 알아챔.
    # 실행취소는 find_all()에서 delete(id:int)를 이용해서 구현할 수 있을 것 같음.
    # 지우개는 하얀색 칠하기 보다 find_overlapping() 혹은 find_closest()를 이용하면 될 것 같음.

    def retrieve_image(self, model):
        ps = self.postscript(colormode='color')
        image = Image.open(io.BytesIO(ps.encode('utf-8')))

        self.sk_data = np.array(image)
        self.sk_tokenized = False
        self.sk_future = image_loader.image_loader.submit(tokenize_sketch_data, model, self.sk_data)
        self.sk_future.add_done_callback(self.__tokenize_sketch_callback)

    
    def __tokenize_sketch_callback(self, sk_future: Future[Image.Image]) :
        try :
            self.sk_data = sk_future.result(timeout=0)
            self.sk_tokenized = True
            print(self.sk_data)
        except Exception as _ :
            self.sk_data = None
            self.sk_tokenized = False
        
    def debug(self):
        print("canvas debug dump")
        for child in self.find_all():
            print(child)
        print(self.type(1))
        print(self.coords(1))

# Load sk_data (numpy array) and preprocecss the sketch.
def tokenize_sketch_data(model, sketch) :
    sk_data = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)

    immean = [0.5, 0.5, 0.5]  # RGB channel mean for imagenet
    imstd = [0.5, 0.5, 0.5]

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(immean, imstd)
    ])

    sk_data = remove_white_space_image(sk_data, 10)
    sk_data = resize_image_by_ratio(sk_data, 224)
    sk_data = make_img_square(sk_data)

    sk_data = transform(sk_data).half()
    sk_data = torch.unsqueeze(sk_data, 0)
    sk_data = sk_data.cuda()

    sk_data, _ = model(sk_data, None, 'test', only_sa=True) 

    return sk_data