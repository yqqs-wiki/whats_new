import re
from dataclasses import dataclass, field

import httpx

from .types import Vers


@dataclass
class Apk:
    url: str
    name: str = field(init=False)
    vers: Vers = field(init=False)

    def __post_init__(self):
        self.name = self.url.split("/")[-1]

        vers = self.name.split("-")[-1].split(".")[:3]
        if len(vers) != 3:
            raise RuntimeError("官网无法获得版本号")

        self.vers = Vers(*vers)


def get_apk():
    r = httpx.get("https://www.chillyroom.com/zh")
    m = re.search(r"https://apk.chillyroom.com/apks/.*?.apk", r.text)
    if m is None:
        raise RuntimeError("官网找不到新版本")
    return Apk(m.group())


def download_apk():
    apk = get_apk()
    print(f"APK名字为{apk.name}")
    with (
        httpx.stream("get", apk.url) as r,
        open(apk.name, mode="wb") as f,
    ):
        for chunk in r.iter_raw():
            f.write(chunk)
