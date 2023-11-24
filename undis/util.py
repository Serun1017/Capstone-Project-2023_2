import os
import platform as _platform
import subprocess

from enum import Enum

import tkinter


class Platform(Enum):
    Windows = "Windows"
    Linux = "Linux"
    MacOS = "Darwin"

    @staticmethod
    def detected() -> "Platform":
        return Platform.from_str(_platform.system())

    @staticmethod
    def from_str(string: str) -> "Platform":
        if string == "Windows":
            return Platform.Windows
        elif string == "Linux":
            return Platform.Linux
        elif string == "Darwin":
            return Platform.MacOS
        else:
            raise ValueError(f"Unknown platform string: {string}")


_detected_platform = Platform.from_str(_platform.system())
if _detected_platform == Platform.Linux:
    _linux_file_explorer = (
        subprocess.run(["xdg-mime", "query", "default", "inode/directory"], capture_output=True).stdout.decode().strip()
    )


class Visibility(Enum):
    """Visibility states of a widget. Can be acquired with `event.state` when binding to the `<Visibility>`."""

    FullyVisible = "VisibilityUnobscured"
    """State when the widget is fully visible."""
    Partial = "VisibilityPartiallyObscured"
    """State when the widget is partially visible and partially obscured."""
    FullyObscured = "VisibilityFullyObscured"
    """State when the widget is fully obscured."""

    @staticmethod
    def is_state_visible(state) -> bool:
        if state == Visibility.FullyObscured:
            return False
        else:
            return True

    @staticmethod
    def is_state_obsucured(state) -> bool:
        if state == Visibility.FullyObscured:
            return True
        else:
            return False


def add_bindtag_to(bindtag_of: tkinter.Misc, to: tkinter.Misc):
    bindtags = list(to.bindtags())
    bindtags.insert(1, bindtag_of.bindtags()[0])
    to.bindtags(tuple(bindtags))


def file_open(path: str):
    """Open a file in the default application for its type."""
    if _detected_platform == Platform.Windows:
        os.startfile(path)  # type: ignore
    elif _detected_platform == Platform.Linux:
        subprocess.call(("xdg-open", path))
    elif _detected_platform == Platform.MacOS:
        subprocess.call(("open", path))


def file_open_in_explorer(path: str):
    """Open a default file explorer with file selected."""
    if _detected_platform == Platform.Windows:
        print(os.path.abspath(path))
        subprocess.call(f'explorer /select,"{os.path.abspath(path)}"')
    elif _detected_platform == Platform.Linux:
        if _linux_file_explorer == "org.kde.dolphin.desktop":
            subprocess.call(["dolphin", "--select", path])
        else:
            subprocess.call(["xdg-open", os.path.split(path)[0]])
    elif _detected_platform == Platform.MacOS:
        subprocess.call(["open", "-R", path])
