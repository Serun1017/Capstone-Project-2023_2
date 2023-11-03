from typing import Self
import requests


class RequestBuilder:
    """
    ## Attributes
    - languages: list[str]
        List of [language codes](https://docs.imagga.com/#multi-language-support) to request.
    """

    def __init__(self, languages: list[str]):
        self.__languages = languages

    @staticmethod
    def default() -> Self:
        """
        Constructs `RequestBuilder` with default attribute values.

        ## Default Attribute Values
        - languages = ["en", "ko"]
        """
        return RequestBuilder(languages=["en", "ko"])

    def auth(self, auth_key: str, auth_secret: str) -> Self:
        self.__auth

    def request_tags(self, image: bytes):
        """
        ## Parameters
        - image: bytes
            Image data in bytes

        ## Returns
        """
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
