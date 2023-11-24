import cv2
import torch

from .data_utils.utils import remove_white_space_image, resize_image_by_ratio, make_img_square
from torchvision.transforms import transforms


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
