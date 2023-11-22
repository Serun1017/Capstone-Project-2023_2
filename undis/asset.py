from PIL import Image
from typing import final


@final
class Asset:
    __BLANK_IMAGE = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    EMPTY_IMAGE = __BLANK_IMAGE
    MISSING_IMAGE = __BLANK_IMAGE

    @staticmethod
    def init():
        try:
            Asset.EMPTY_IMAGE = Image.open("assets/Empty-Image.png")
        finally:
            pass
        try:
            Asset.MISSING_IMAGE = Image.open("assets/Missing-Image.png")
        finally:
            pass
