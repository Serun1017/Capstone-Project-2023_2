"""
Constants from config
"""


from typing import Final
import toml


_config_file_path = "config.toml"
_config_file = toml.load(_config_file_path)
# debug
print(_config_file)
print(toml.dumps(_config_file))


IMAGGA_KEY: Final[str] = _config_file["Imagga"]["key"]
IMAGGA_SECRET: Final[str] = _config_file["Imagga"]["secret"]

