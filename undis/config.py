"""
Constants from config
"""


from typing import Final
import toml


_config_file_path = "config.toml"
_config_file = toml.load(_config_file_path)

IMAGGA_KEY: Final[str] = _config_file["Imagga"]["key"]
IMAGGA_SECRET: Final[str] = _config_file["Imagga"]["secret"]

del _config_file_path
del _config_file
