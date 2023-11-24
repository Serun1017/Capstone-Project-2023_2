import os
from PIL import Image
from typing import final

from . import util


@final
class Asset:
    __BLANK_IMAGE = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    EMPTY_IMAGE = __BLANK_IMAGE
    MISSING_IMAGE = __BLANK_IMAGE
    SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

    @staticmethod
    def init():
        try:
            Asset.EMPTY_IMAGE = Image.open(util.path_from_root("assets", "Empty-Image.png"))
        except Exception as _:
            pass
        try:
            Asset.MISSING_IMAGE = Image.open(util.path_from_root("assets", "Missing-Image.png"))
        except Exception as _:
            pass
        supported_extensions = [
            extension
            for extension, format_name in Image.registered_extensions().items()
            if format_name in Image.OPEN and format_name in Image.SAVE
        ]
        # remove and insert to front the most common extensions to improve performance
        for extension in Asset.SUPPORTED_IMAGE_EXTENSIONS:
            supported_extensions.remove(extension)
        for extension in reversed(Asset.SUPPORTED_IMAGE_EXTENSIONS):
            supported_extensions.insert(0, extension)
        Asset.SUPPORTED_IMAGE_EXTENSIONS = supported_extensions


Asset.init()
