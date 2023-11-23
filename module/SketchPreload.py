import cv2
import numpy as np
import torch

from data_utils.dataset import ValidSet
from torch.utils.data import DataLoader, Dataset
from data_utils.utils import remove_white_space_image, resize_image_by_ratio, make_img_square
from torchvision.transforms import transforms
from options import Option
from ModelLoad import ModelLoader

class SketchLoader :
    def __init__(self, model, args) :
        self.model = model
        self.args = args
        self.sk_data = None

    # Load sk_data (numpy array) and preprocecss the sketch.
    def LoadSketch(self, sk_data) :
        self.sk_data = cv2.cvtColor(sk_data, cv2.COLOR_BGR2RGB)

        immean = [0.5, 0.5, 0.5]  # RGB channel mean for imagenet
        imstd = [0.5, 0.5, 0.5]

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(immean, imstd)
        ])

        self.sk_data = remove_white_space_image(self.sk_data, 10)
        self.sk_data = resize_image_by_ratio(self.sk_data, 224)
        self.sk_data = make_img_square(self.sk_data)

        self.sk_data = transform(self.sk_data).half()
        self.sk_data = torch.unsqueeze(self.sk_data, 0)
        self.sk_data = self.sk_data.cuda()

        self.sk_data, _ = self.model(self.sk_data, None, 'test', only_sa=True)

if __name__ == "__main__" :
    args = Option().parse()
    model = ModelLoader(args)

    ### Test Image Loaded to img
    path = 'C:\\Users\\tjgh2\\OneDrive\\바탕 화면\\capstone\\Capstone Project\\datasets\\raster_sketches\\1\\000000006336.jpg'
    image_path = np.fromfile(path, np.uint8)
    img = cv2.imdecode(image_path, cv2.IMREAD_COLOR)

    # Start SketchLoader
    sketch = SketchLoader(model, args)
    
    sketch.LoadSketch(img)
    print(sketch.sk_data)
