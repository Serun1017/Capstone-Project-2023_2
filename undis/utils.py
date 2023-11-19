import os
import platform
import subprocess

_detected_platform = platform.system()
if _detected_platform == "Linux":
    _linux_file_explorer = (
        subprocess.run(
            ["xdg-mime", "query", "default", "inode/directory"], capture_output=True
        )
        .stdout.decode()
        .strip()
    )


def file_open(path: str):
    """Open a file in the default application for its type."""
    if _detected_platform == "Windows":
        os.startfile(path)
    elif _detected_platform == "Linux":
        subprocess.call(("xdg-open", path))
    elif _detected_platform == "Darwin":
        subprocess.call(("open", path))


def file_open_in_explorer(path: str):
    """Open a default file explorer with file selected."""
    if _detected_platform == "Windows":
        subprocess.call(["explorer", "/select,", f'"{path}"'])
    elif _detected_platform == "Linux":
        if _linux_file_explorer == "org.kde.dolphin.desktop":
            subprocess.call(["dolphin", "--select", path])
        else:
            subprocess.call(["xdg-open", os.path.split(path)[0]])
    elif _detected_platform == "Darwin":
        subprocess.call(["open", "-R", path])
