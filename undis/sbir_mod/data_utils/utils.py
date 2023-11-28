import numpy as np
from PIL import Image
from torchvision.transforms import transforms
import cv2


def preprocess(image_path, img_type="im"):
    # immean = [0.485, 0.456, 0.406]  # RGB channel mean for imagenet
    # imstd = [0.229, 0.224, 0.225]

    immean = [0.5, 0.5, 0.5]  # RGB channel mean for imagenet
    imstd = [0.5, 0.5, 0.5]

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(immean, imstd)])

    if img_type == "im":
        return transform(Image.open(image_path).resize((224, 224)).convert("RGB"))
    else:
        # sketch crop， 224
        # 한글 경로 문제
        image_path = np.fromfile(image_path, np.uint8)
        img = cv2.imdecode(image_path, cv2.IMREAD_COLOR)

        # img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = remove_white_space_image(img, 10)
        img = resize_image_by_ratio(img, 224)
        img = make_img_square(img)

        return transform(img)


def remove_white_space_image(img_np: np.ndarray, padding: int):
    """
    :param img_np:
    :return:
    """
    # if np.max(img_np) <= 1.0:  # 1.0 <= 1.0 True
    #     img_np = (img_np * 255).astype("uint8")
    # else:
    #     img_np = img_np.astype("uint8")

    h, w, c = img_np.shape
    img_np_single = np.sum(img_np, axis=2)
    Y, X = np.where(img_np_single <= 300)  # max = 300
    ymin, ymax, xmin, xmax = np.min(Y), np.max(Y), np.min(X), np.max(X)
    img_cropped = img_np[
        max(0, ymin - padding) : min(h, ymax + padding),  # type: ignore
        max(0, xmin - padding) : min(w, xmax + padding),  # type: ignore
        :,
    ]
    return img_cropped


def resize_image_by_ratio(img_np: np.ndarray, size: int):
    """
    :param img_np:
    :param size:
    :return:
    """
    # print(len(img_np.shape))
    if len(img_np.shape) == 2:
        h, w = img_np.shape
    elif len(img_np.shape) == 3:
        h, w, _ = img_np.shape
    else:
        assert 0

    ratio = h / w  # type: ignore
    if h > w:  # type: ignore
        new_img = cv2.resize(
            img_np,
            (
                int(size / ratio),
                size,
            ),
        )  # resize is w, h  (fx, fy...)
    else:
        new_img = cv2.resize(
            img_np,
            (
                size,
                int(size * ratio),
            ),
        )
    # new_img[np.where(new_img < 200)] = 0
    return new_img


def make_img_square(img_np: np.ndarray):
    if len(img_np.shape) == 2:
        h, w = img_np.shape
        if h > w:
            delta1 = (h - w) // 2
            delta2 = (h - w) - delta1

            white1 = np.ones((h, delta1)) * np.max(img_np)
            white2 = np.ones((h, delta2)) * np.max(img_np)

            new_img = np.hstack([white1, img_np, white2])
            return new_img
        else:
            delta1 = (w - h) // 2
            delta2 = (w - h) - delta1

            white1 = np.ones((delta1, w)) * np.max(img_np)
            white2 = np.ones((delta2, w)) * np.max(img_np)

            new_img = np.vstack([white1, img_np, white2])
            return new_img
    if len(img_np.shape) == 3:
        h, w, c = img_np.shape
        if h > w:
            delta1 = (h - w) // 2
            delta2 = (h - w) - delta1

            white1 = np.ones((h, delta1, c), dtype=img_np.dtype) * np.max(img_np)
            white2 = np.ones((h, delta2, c), dtype=img_np.dtype) * np.max(img_np)

            new_img = np.hstack([white1, img_np, white2])
            return new_img
        else:
            delta1 = (w - h) // 2
            delta2 = (w - h) - delta1

            white1 = np.ones((delta1, w, c), dtype=img_np.dtype) * np.max(img_np)
            white2 = np.ones((delta2, w, c), dtype=img_np.dtype) * np.max(img_np)

            new_img = np.vstack([white1, img_np, white2])
            return new_img


def create_dict_texts(texts):
    texts = list(texts)
    dicts = {l: i for i, l in enumerate(texts)}
    return dicts
