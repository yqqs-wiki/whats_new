import os
import re
from datetime import date
from typing import TYPE_CHECKING

from mwclient import Site

from .types import Vers

if TYPE_CHECKING:
    from .chillyroom import Apk


class Wiki:
    def __init__(self):
        self.vers: Vers
        self.site = Site("yqqs.huijiwiki.com")
        password = os.environ.get("HUIJIWIKI_PASSWORD")
        self.site.login("慕棱", password)

    def get_text(self, name="更新日志"):
        self.whats_new = self.site.pages[name]
        return self.whats_new.text()

    def find_vers(self, text: str) -> re.Match:
        if m := re.search(r"==(\d).(\d).(\d)", text):
            self.vers = Vers(*m.groups())
            return m

        raise RuntimeError("维基找不到旧版本号")

    def insert_whats_new(self, apk: "Apk", whats_new: str):
        text = self.get_text()
        m = self.find_vers(text)

        if tuple(map(int, apk.vers)) <= tuple(map(int, self.vers)):
            print("已是最新版本")
            return

        today = date.today()
        vers_str = ".".join(apk.vers)
        today_str = today.strftime("%Y.%m.%d")
        content = "\n\n".join(
            (
                f"=={vers_str}版本==\n{today_str}",
                f"[{apk.url} {vers_str}安卓官网包下载]",
                whats_new,
                "",
            )
        )

        print(f"将更新至{vers_str}版本")

        insert_index = m.span()[0]
        self.whats_new.edit(
            text[:insert_index] + content + text[insert_index:], bot=False
        )
