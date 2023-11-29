from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from typing import final

from .sbir_mod.ModelLoad import load_model
from .sbir_mod.options import Option
from . import util


asset_loader = ThreadPoolExecutor(max_workers=4)


@final
class Asset:
    __BLANK_IMAGE = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    EMPTY_IMAGE = __BLANK_IMAGE
    MISSING_IMAGE = __BLANK_IMAGE
    SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
    MODEL = asset_loader.submit(lambda: load_model(Option().parse()))

    @staticmethod
    def init():
        try:
            Asset.EMPTY_IMAGE = Image.open(util.path_from_root("assets", "Empty-Image.png"))
        except Exception as _:
            pass
        try:
            Asset.MISSING_IMAGE = Image.open(util.path_from_root("assets", "Missing-Image.png"))
        except Exception as _:
            print("Placeholder image is missing.")
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
