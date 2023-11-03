from typing import final, Self
import requests


@final
class RequestBuilder:
    """## Example
    ```py
    request_builder = RequestBuilder.default()
    ```
    """

    __languages: list[str]

    def __init__(self, languages: list[str]):
        self.__languages = languages

    @classmethod
    def default(cls) -> "RequestBuilder":
        instance = cls(languages=["en", "ko"])
        return instance

    def auth(self, auth_key: str, auth_secret: str) -> Self:
        return self

    def request_tags(self, image: bytes):
        """ """
        post_form = {"language": ",".join(self.__languages)}
        requests.post("https://api.imagga.com/v2/tags", data=post_form)
        pass

    def request_colors(self, image: bytes):
        """
        Requests colors from Imagga. All of the builder attributes are ignored.

        ## Parameters
        - image: bytes
            Image data in bytes

        ## Returns
        """
        post_form = {}
        requests.post("https://api.imagga.com/v2/tags", data=post_form)
