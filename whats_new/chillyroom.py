import re

import httpx


def get_apk_url():
    r = httpx.get("https://www.chillyroom.com/zh")
    m = re.search(r"https://apk.chillyroom.com/apks/.*?.apk", r.text)
    if m is None:
        raise RuntimeError("官网找不到新版本")
    return m.group()


def extract_vers(apk_url: str):
    return tuple(
        int(ver) for ver in apk_url.split("/")[-1].split("-")[-1].split(".")[:3]
    )
