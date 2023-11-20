from PIL import Image
from typing import final


@final
class Asset:
    EMPTY_IMAGE = Image.open("assets/Empty-Image.png")
