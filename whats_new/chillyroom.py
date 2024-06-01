import re
from dataclasses import dataclass, field
from typing import NamedTuple

import httpx


class Vers(NamedTuple):
    major: int
    minor: int
    patch: int


@dataclass
class Apk:
    url: str
    vers: tuple[int, int, int] = field(init=False)

    def __post_init__(self):
        vers = [
            int(ver) for ver in self.url.split("/")[-1].split("-")[-1].split(".")[:3]
        ]
        if len(vers) != 3:
            raise RuntimeError("官网无法获得版本号")

        self.vers = Vers(*vers)


def get_apk():
    r = httpx.get("https://www.chillyroom.com/zh")
    m = re.search(r"https://apk.chillyroom.com/apks/.*?.apk", r.text)
    if m is None:
        raise RuntimeError("官网找不到新版本")
    return Apk(m.group())
