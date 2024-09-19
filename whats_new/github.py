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
    old_ver = environ.get("OLD_VER")
    if not old_ver:
        raise RuntimeError("无法获得旧版本号")
    print(f"旧版本为：{old_ver}")

    if tuple(map(int, apk.vers)) > tuple(map(int, old_ver.split("."))):
        new_ver = ".".join(apk.vers)
        print(f"将创建发行版：{new_ver}")
        set_github_output({"need_upload": 1, "new_ver": new_ver})
        return True
    else:
        print("不需要创建发行版")
        return False
