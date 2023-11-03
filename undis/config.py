"""
Parses constants from `config.toml` file
"""

from typing import Final as _Final
import toml as _toml


_config_file_path = "config.toml"
_config_file = _toml.load(_config_file_path)

IMAGGA_KEY: _Final[str] = _config_file["Imagga"]["key"]
IMAGGA_SECRET: _Final[str] = _config_file["Imagga"]["secret"]

del _config_file_path
del _config_file
