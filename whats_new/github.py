from os import environ
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chillyroom import Apk


def set_github_output(d: dict):
    if output_path := environ.get("GITHUB_OUTPUT"):
        with open(output_path, "a") as out:
            for name, value in d.items():
                out.write(f"{name}={value}\n")


def check_release_needed(apk: "Apk"):
    if tuple(map(int, apk.vers)) > tuple(
        map(int, environ.get("git_tag", "").split("."))
    ):
        new_vers_str = ".".join(apk.vers)
        print(f"将创建发行版：{new_vers_str}")
        set_github_output({"need_upload": 1, "new_vers": new_vers_str})
        return True
    else:
        print("不需要创建发行版")
        return False
