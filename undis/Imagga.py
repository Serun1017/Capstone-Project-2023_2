"""
## Example

```py
import Imagga
image = b"text instead of image"
response = imagga.RequestBuilder.default().request_tags(image)
```
"""

from typing import final as _final, Self as _Self, Any as _Any
import requests as _requests

from . import config as _config


@_final
class RequestBuilder:
    __languages: list[str]
    __auth: tuple[str, str]

    def __init__(self, languages: list[str]):
        self.__languages = languages
        self.__auth = (_config.IMAGGA_KEY, _config.IMAGGA_SECRET)

    @classmethod
    def default(cls) -> "RequestBuilder":
        """Construct `RequestBuilder` with default attributes."""
        instance = cls(languages=["en"])
        return instance

    def add_language(self, language: str) -> _Self:
        """Adds language to tags request. [Supported languages](https://docs.imagga.com/#multi-language-support)."""
        self.__languages.append(language)
        return self

    def request_tags(self, image: bytes) -> _Any:
        """Requests tags from Imagga."""

        post_form = {"language": ",".join(self.__languages), "image": image}
        response = _requests.post(
            # "https://httpbin.org/post",  # debug url
            "https://api.imagga.com/v2/tags",
            auth=self.__auth,
            data=post_form,
        )
        return response.json()

    def request_colors(self, image: bytes) -> _Any:
        """Requests colors from Imagga."""

        post_form = {}
        response = _requests.post(
            # "https://httpbin.org/post",  # debug url
            "https://api.imagga.com/v2/colors",
            auth=self.__auth,
            data=post_form,
        )
        return response.json()
